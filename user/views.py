from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.http import HttpRequest

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


def add_user_view(request:HttpRequest):
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


# تعديل مستخدم
def update_user_view(request:HttpRequest, user_id):
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
