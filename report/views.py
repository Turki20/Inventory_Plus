from django.shortcuts import render
from django.http import HttpRequest
from product.models import Product, Category
from supplier.models import Supplier
from purchases_sales.models import Purchase, Sale
from django.db.models import F, Sum
from django.core.paginator import Paginator

import json
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required(login_url='/accounts/sign_in/')
@staff_member_required
def report_view(request:HttpRequest):
        
    # المنتجات التي وصلت الى حد التنبيه
    low_stock_products = Product.objects.filter(quantity_in_stock__lte=F('min_quantity_alert')) # lte: اقل من او يساوي
    
    page = request.GET.get('page', 1) 
    paginator = Paginator(low_stock_products, 5) 
    low_stock_products = paginator.get_page(page) 
    
    
    # قيمه تكلفة كل المنتجات في المخزون
    stock_value = Product.objects.aggregate(
        total_value=Sum(F('quantity_in_stock') * F('cost_price'))
    )
    
    # الارباح
    # نجمع لكل المبيعات ناتج ضرب الكميه في صافي الربح
    profits = Sale.objects.aggregate(total_profit=Sum((F('product__selling_price') - F('product__cost_price')) * F('quantity')))
    
    # اكثر عشر منتجات مبيعا
    top_selling_products = Sale.objects.values('product__name').annotate(
    total_sold=Sum('quantity')
    ).order_by('-total_sold')[:10]

    top_products_list = list(top_selling_products)
    top_products_json = json.dumps(top_products_list, cls=DjangoJSONEncoder)
    
    # مقارنه المشتريات بالمبيعات
    sales_vs_purchases = Product.objects.annotate(
    total_sold=Sum('sale__quantity'),
    total_purchased=Sum('purchase__quantity')
    ).values('name', 'total_sold', 'total_purchased')[:6]

    sales_vs_purchases_list = list(sales_vs_purchases)
    sales_vs_purchases_json = json.dumps(sales_vs_purchases_list, cls=DjangoJSONEncoder)
    
    # اكثر عشر موردين تعاملا
    top_suppliers = Purchase.objects.values('supplier__name').annotate(
    total_orders=Sum('quantity'),
    total_amount=Sum(F('quantity') * F('product__cost_price'))
    ).order_by('-total_orders')[:10]
    
    print(top_suppliers)
    
    context ={
        'low_stock_products':low_stock_products,
        'stock_value':stock_value,
        'profits': profits,
        'top_products_json': top_products_json,
        'sales_vs_purchases_json': sales_vs_purchases_json,
        'top_suppliers':top_suppliers,
    }
    return render(request, 'report/index.html', context)