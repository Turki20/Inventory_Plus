from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.http import HttpRequest
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required


@login_required(login_url='accounts/sign_in/')
@staff_member_required
def all_users(request):
    if request.method == 'POST':
        search = request.POST.get('search', '')
        order_by = request.POST.get('order_by', 'none')

        users = User.objects.filter(username__icontains=search)

        if order_by != 'none':
            if order_by == 'latest':
                users = users.order_by('-date_joined')
            else:
                users = users.order_by('date_joined')
    else:
        users = User.objects.all()
        
    number_of_users = users.count()
    return render(request, 'user/all_users.html', {"users": users, 'number_of_users':number_of_users})

@login_required(login_url='accounts/sign_in/')
@staff_member_required
def add_user_view(request:HttpRequest):
    if not request.user.is_superuser:
        return render(request, "main/index.html", {"show_permission_modal": True})
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        is_superuser = request.POST.get('is_superuser')    

        if not username or not password:
            messages.error(request, 'Username and password are required', 'alert-danger')
            return redirect('user:add_user_view')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists', 'alert-danger')
            return redirect('user:add_user_view')

        if is_superuser == 'true':
            User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name, is_superuser=True, is_staff=True)
        else:
            User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name, is_staff=True)
        messages.success(request, 'User added successfully', 'alert-success')
        return redirect('user:all_users_view')

    return render(request, 'user/add_user.html')

@login_required(login_url='accounts/sign_in/')
@staff_member_required
def update_user_view(request:HttpRequest, user_id):
    if not request.user.is_superuser:
        return render(request, "main/index.html", {"show_permission_modal": True})

    user = get_object_or_404(User, pk=user_id)

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        if not username:
            messages.error(request, 'Username is required', 'alert-danger')
            return redirect('user:update_user_view', user_id)

        if User.objects.exclude(pk=user_id).filter(username=username).exists():
            messages.error(request, 'Another user with this username already exists', 'alert-danger')
            return redirect('user:update_user_view', user_id)

        user.username = username
        user.email = email
        user.first_name = first_name
        user.last_name = last_name

        if password:
            user.password = make_password(password) # convert to hash 

        user.save()

        messages.success(request, 'User updated successfully', 'alert-success')
        return redirect('user:all_users_view')

    return render(request, 'user/update_user.html', {"user_obj": user})

@login_required(login_url='accounts/sign_in/')
@staff_member_required
def delete_user(request:HttpRequest, user_id):
    if not request.user.is_superuser:
        return render(request, "main/index.html", {"show_permission_modal": True})
    
    try:
        User.objects.get(pk = user_id).delete()
        messages.success(request, 'The User has been successfully removed.', 'alert-success')
        return redirect('user:all_users_view')

    except Exception as e:
        messages.error(request, 'An error occurred while deleting.', 'alert-danger')
        return redirect('user:all_users_view')
    