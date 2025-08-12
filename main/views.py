from django.shortcuts import render
from django.http import HttpRequest
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='accounts/sign_in/')
@staff_member_required
def index_view(request:HttpRequest):
    
    return render(request, 'main/index.html', {})