from django.shortcuts import render, redirect
from django.http import HttpRequest
from .models import Product, Category
from django.db.models import Sum, F
from django.contrib import messages
from django.core.paginator import Paginator
# Create your views here.


def all_products_view(request:HttpRequest):
    
    if request.method == 'POST':
        search = request.POST['search']
        order_by = request.POST['order_by']
        category = request.POST['category']
        products = Product.objects.filter(name__icontains=search)
        if category != 'all':
            products = products.filter(category=Category.objects.get(name=category))
        
        if order_by != 'none':
            if order_by == 'highest':
                products = products.order_by('-cost_price')
            else:
                products = products.order_by('cost_price')

    else:
        products = Product.objects.all()
        
    number_of_products = products.count()
    products = products.annotate(total_cost =F('quantity_in_stock') * F('cost_price'))
    total_inventory_cost = products.aggregate(Sum('total_cost'))
    
    
    # pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(products, 8)
    products = paginator.get_page(page)
    
    print(paginator)
    
    context = {
        "products":products, 
        'number_of_products': number_of_products,
        "total_inventory_cost": total_inventory_cost,
        'all_categories': Category.objects.all(),
    }
    return render(request, 'product/all_products.html', context)

def add_product_view(request:HttpRequest):
    
    if request.method == 'POST':
        name = request.POST.get('name')
        sku = request.POST.get('sku')
        image = request.FILES.get('image') 
        category_id = request.POST.get('category')
        supplier_id = request.POST.get('supplier') 
        description = request.POST.get('description') 

        quantity = request.POST.get('quantity_in_stock')
        cost_price = request.POST.get('cost_price')
        selling_price = request.POST.get('selling_price')

        if not all([name, sku, category_id, quantity, cost_price, selling_price]):
            messages.error(request, 'Some fields are missing', 'alert-danger')
            return redirect('product:add_product_view')

        try:
            category = Category.objects.get(name=category_id)
        except Category.DoesNotExist:
            messages.error(request, 'category does not exisit', 'alert-danger')
            return redirect('product:add_product_view')

        supplier = None

        if image is not None:
            Product.objects.create(
                name=name,
                sku=sku,
                image=image,
                category=category,
                supplier=supplier,
                description=description,
                quantity_in_stock=int(quantity),
                cost_price=float(cost_price),
                selling_price=float(selling_price)
            )
        else:
            Product.objects.create(
                name=name,
                sku=sku,
                category=category,
                supplier=supplier,
                description=description,
                quantity_in_stock=int(quantity),
                cost_price=float(cost_price),
                selling_price=float(selling_price)
            )
        
        messages.success(request, 'The product has been added successfully.', 'alert-success')
        return redirect('product:add_product_view') 

    
    all_categories = Category.objects.all()
    return render(request, 'product/add_product.html', {'all_categories': all_categories})


def product_detail_view(request:HttpRequest, product_id):
    
    product = Product.objects.get(pk = product_id)
    
    return render(request, 'product/detail.html', {'product':product})

def delete_product(request:HttpRequest, product_id):
    
    try:
        Product.objects.get(pk = product_id).delete()
        messages.success(request, 'The product has been successfully removed.', 'alert-success')
        return redirect('product:all_products_view')

    except Exception as e:
        messages.error(request, 'An error occurred while deleting.', 'alert-danger')
        return redirect('product:all_products_view')
    
def update_product_view(request:HttpRequest, product_id:int):
    if request.method == 'POST':
        id = request.POST.get('id')
        name = request.POST.get('name')
        sku = request.POST.get('sku')
        image = request.FILES.get('image') 
        category_id = request.POST.get('category')
        supplier_id = request.POST.get('supplier') 
        description = request.POST.get('description') 

        quantity = request.POST.get('quantity_in_stock')
        cost_price = request.POST.get('cost_price')
        selling_price = request.POST.get('selling_price')

        print(category_id)
        
        if not all([name, sku, category_id, quantity, cost_price, selling_price]):
            messages.error(request, 'Some fields are missing', 'alert-danger')
            return redirect('product:update_product_view', id)

        try:
            category = Category.objects.get(pk=category_id)
        except Category.DoesNotExist:
            messages.error(request, 'category does not exisit', 'alert-danger')
            return redirect('product:update_product_view', id)

        supplier = None

        if image is not None:
            product = Product.objects.get(pk = int(id))
            product.name=name
            product.sku=sku
            product.image=image
            product.category=category
            product.supplier=supplier
            product.description=description
            product.quantity_in_stock=int(quantity)
            product.cost_price=float(cost_price)
            product.selling_price=float(selling_price)
            product.save()
        else:
            product = Product.objects.get(pk = int(id))
            product.name=name
            product.sku=sku
            product.category=category
            product.supplier=supplier
            product.description=description
            product.quantity_in_stock=int(quantity)
            product.cost_price=float(cost_price)
            product.selling_price=float(selling_price)
            product.save()
        
        messages.success(request, 'The product has been updated successfully.', 'alert-success')
        return redirect('product:product_detail_view', id) 
    
    product = Product.objects.get(pk = product_id)
    all_categories = Category.objects.all()

    return render(request, 'product/update_product.html', {"product": product, 'all_categories': all_categories})


