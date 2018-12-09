from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import product
from . import forms


def products_all(request):
    product_blog = product.objects.all()
    return render(request, 'marketplace/productsblog.html',{'products':product_blog})

def product_details(request, slug):
    pro_details = product.objects.get(pk=slug)
    return render(request, 'marketplace/product_details.html', {'details':pro_details})

@login_required(login_url="http://127.0.0.1:8000/register/login/")

def add_product(request):
    if request.method == "POST":
        form = forms.productform(request.POST,request.FILES)
        if form.is_valid():
            product_instance = form.save(commit=False)
            product_instance.fullname = request.user
            product_instance.save()
            return redirect('marketplace:products_blog')


    else:
        form = forms.productform()
    return render(request, 'marketplace/product_add.html',{'form':form})
@login_required(login_url="http://127.0.0.1:8000/register/login/")
def my_products(request):
    uname = request.user
    my_product = product.objects.filter(fullname = uname)
    return render(request, 'marketplace/my_products.html',{'my_pro':my_product})
@login_required(login_url="http://127.0.0.1:8000/register/login/")
def edit_product(request, id = None):
    instance= get_object_or_404(product, pk= id)
    form= forms.productform(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('marketplace:products_blog')
    context={
        'form':form,
    }
    return render(request, 'marketplace/edit_product.html',{'form':form})

@login_required(login_url="http://127.0.0.1:8000/register/login/")
def delete_product(request, id):
    instance= get_object_or_404(product, pk= id)
    instance.delete()
    return redirect('marketplace:products_blog')
