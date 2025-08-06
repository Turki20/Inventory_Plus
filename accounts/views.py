from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# Create your views here.


def sign_in_view(request:HttpRequest):
    
    if request.method == 'POST':
        user = authenticate(request, username = request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('main:index_view')
        else:
            messages.error(request, 'The password or username is incorrect', 'alert-danger')
            return redirect('accounts:sign_in_view')
    
    return render(request, 'accounts/sign_in.html', {})