from django.db.models import F, Sum
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from .models import Supplier
from django.contrib import messages

def all_suppliers_view(request: HttpRequest):
    if request.method == 'POST':
        search = request.POST.get('search', '')
        order_by = request.POST.get('order_by', 'none')

        suppliers = Supplier.objects.filter(name__icontains=search)

        if order_by != 'none':
            if order_by == 'latest':
                suppliers = suppliers.order_by('-created_at')
            else:
                suppliers = suppliers.order_by('created_at')
    else:
        suppliers = Supplier.objects.all()

    number_of_suppliers = suppliers.count()

    # pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(suppliers, 8)  # 8 suppliers per page
    suppliers = paginator.get_page(page)

    context = {
        "suppliers": suppliers,
        'number_of_suppliers': number_of_suppliers,
    }
    return render(request, 'supplier/all_suppliers.html', context)



def add_supplier_view(request: HttpRequest):

    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address')
        website = request.POST.get('website')

        # التحقق من الحقول المطلوبة
        if not all([name, phone]):
            messages.error(request, 'Supplier name and phone is required', 'alert-danger')
            return redirect('supplier:add_supplier_view')

        # إنشاء المورد
        Supplier.objects.create(
            name=name,
            phone=phone,
            email=email,
            address=address,
            website=website
        )

        messages.success(request, 'The supplier has been added successfully.', 'alert-success')
        return redirect('supplier:add_supplier_view')

    return render(request, 'supplier/add_supplier.html')


def update_supplier_view(request: HttpRequest, supplier_id: int):
    supplier = get_object_or_404(Supplier, pk=supplier_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        if not all([name, phone]):
            messages.error(request, 'Some required fields are missing', 'alert-danger')
            return redirect('supplier:update_supplier_view', supplier_id)

        supplier.name = name
        supplier.email = email
        supplier.phone = phone
        supplier.address = address
        supplier.save()

        messages.success(request, 'The supplier has been updated successfully.', 'alert-success')
        return redirect('supplier:all_suppliers_view')

    return render(request, 'supplier/update_supplier.html', {"supplier": supplier})


def delete_supplier(request:HttpRequest, supplier_id):
    
    try:
        Supplier.objects.get(pk = supplier_id).delete()
        messages.success(request, 'The Supplier has been successfully removed.', 'alert-success')
        return redirect('supplier:all_suppliers_view')

    except Exception as e:
        messages.error(request, 'An error occurred while deleting.', 'alert-danger')
        return redirect('supplier:all_suppliers_view')
    