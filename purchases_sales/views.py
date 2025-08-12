from django.shortcuts import render, redirect
from django.http import HttpRequest
from .models import Purchase, Sale
from product.models import Product
from supplier.models import Supplier
from django.contrib import messages
from django.core.paginator import Paginator

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required

from Inventory_Plus import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from django.contrib.auth.models import User


# Create your views here.

@login_required(login_url='accounts/sign_in/')
@staff_member_required
def purchases_sales_view(request:HttpRequest):
    sales = Sale.objects.all()
    purchases = Purchase.objects.all()
    
    page_sale = request.GET.get('page_sale', 1)
    paginator = Paginator(sales, 5)
    sales = paginator.get_page(page_sale)
    
    page_purchases = request.GET.get('page_purchases', 1)
    paginator = Paginator(purchases, 5)
    purchases = paginator.get_page(page_purchases)

    return render(request, 'purchases_sales/purchases_sales.html', {'purchases':purchases, 'sales':sales})

@login_required(login_url='accounts/sign_in/')
@staff_member_required
def add_purchase_view(request:HttpRequest):
    
    if request.method == "POST":
        product_id = request.POST['product']
        supplier_id = request.POST.get('supplier')
        quantity = int(request.POST['quantity'])

        if quantity <= 0:
            messages.error(request, 'quantity must be greater than 0.', 'alert-danger')
            return redirect('purchases_sales:add_purchase_view')
    
        try:
            product = Product.objects.get(id=product_id)
            supplier = Supplier.objects.get(id=supplier_id) if supplier_id else None

            Purchase.objects.create(
                product=product,
                supplier=supplier,
                quantity=quantity,
                created_by=request.user
            )
            
        except Exception as e:
            messages.error(request, 'An error occurred.', 'alert-danger')
            return redirect('purchases_sales:add_purchase_view')
    

        product.quantity_in_stock += quantity
        product.save()
        messages.success(request, "Purchase added successfully." , 'alert-success')
        return redirect('purchases_sales:add_purchase_view')
    
    all_products = Product.objects.all()
    all_suppliers = Supplier.objects.all()
    return render(request, 'purchases_sales/add_purchase.html', {'all_products':all_products, 'all_suppliers':all_suppliers})

@login_required(login_url='accounts/sign_in/')
@staff_member_required
def add_sale_view(request:HttpRequest):
    if request.method == 'POST':
        product_id = request.POST.get('product')
        quantity = int(request.POST.get('quantity'))
        customer_name = request.POST.get('customer_name', '')
        try:
            product = Product.objects.get(id=product_id)

            if product.quantity_in_stock < quantity:
                messages.error(request, f'The required quantity is not available, the available quantity is {product.quantity_in_stock}', 'alert-danger')
                return redirect('purchases_sales:add_sale_view')
            
            Sale.objects.create(
                product=product,
                quantity=quantity,
                customer_name=customer_name,
                created_by=request.user
            )
            
            product.quantity_in_stock -= quantity
            product.save()
            
            if product.quantity_in_stock < product.min_quantity_alert:
                content_html = render_to_string('mail/low_stock_alert.html', {
                    'product_name': product.name,
                    'product_image': product.image.url if product.image else '',
                    'product_quantity': product.quantity_in_stock
                })
                all_superusers_email = list(
                    User.objects.filter(is_superuser=True).values_list('email', flat=True)
                )
                email = EmailMessage("Low Stock Alert", content_html, settings.EMAIL_HOST_USER, all_superusers_email)
                email.content_subtype = 'html'
                email.send()
            
        except Exception as e:
            print(e)
            messages.error(request, 'An error occurred.', 'alert-danger')
            return redirect('purchases_sales:add_sale_view')
        
        
        messages.success(request, "Sale added successfully!", 'alert-success')
        return redirect('purchases_sales:add_sale_view')

    all_products = Product.objects.all()
    return render(request, 'purchases_sales/add_sale.html', {'all_products': all_products})

@login_required(login_url='accounts/sign_in/')
@staff_member_required
def delete_sale(request:HttpRequest, sale_id):
    try:
        Sale.objects.get(pk = sale_id).delete()
        messages.success(request, 'The Sale has been successfully removed.', 'alert-success')
        return redirect('purchases_sales:purchases_sales_view')

    except Exception as e:
        messages.error(request, 'An error occurred while deleting.', 'alert-danger')
        return redirect('purchases_sales:purchases_sales_view')
    
@login_required(login_url='accounts/sign_in/')
@staff_member_required   
def delete_purchase(request:HttpRequest, purchase_id):
    try:
        Purchase.objects.get(pk = purchase_id).delete()
        messages.success(request, 'The Purchase has been successfully removed.', 'alert-success')
        return redirect('purchases_sales:purchases_sales_view')

    except Exception as e:
        messages.error(request, 'An error occurred while deleting.', 'alert-danger')
        return redirect('purchases_sales:purchases_sales_view')