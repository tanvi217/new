from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
#from marketplace.serializer import products_boughtSerializer #
from rest_framework.views import APIView
from .models import product, Order, OrderItem ,Transaction
from . import forms
from django.contrib import messages
from django.template.loader import render_to_string
import datetime
import stripe
from .extras import generate_order_id, transact, generate_client_token

def test(request):
    product_blog = product.objects.all()
    return render(request, 'marketplace/test.html',{'products':product_blog})

def get_user_pending_order(request):
    # get order for the correct user
    order = Order.objects.filter(user=request.user, is_ordered=False)
    if order.exists():
        # get the only order in the list of filtered orders
        return order[0]
    return 0

def products_all(request):
    product_blog = product.objects.all()
    return render(request, 'marketplace/blog.html',{'products':product_blog})

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
        context={
        'form':form,
        'heading': "Add Product",
        }
    return render(request, 'marketplace/product_add.html',context)


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
        'heading': "Edit Product",
    }
    return render(request, 'marketplace/product_add.html',context)

@login_required(login_url="http://127.0.0.1:8000/register/login/")
def delete_product(request, id):
    instance= get_object_or_404(product, pk= id)
    instance.delete()
    return redirect('marketplace:products_blog')
# django API
'''
class productsListView(APIView):
    def get(self,request):
        product_delivered = Transcation.objects.all()
        serializer = products_boughtSerializer(product_delivered,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = products_boughtSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)
'''
def add_to_cart(request, id):
    if request.method == "POST":
        prod = product.objects.get(id=id)
        user_order, status = Order.objects.get_or_create(user=request.user, is_ordered=False)
        if status:
            ref_code = generate_order_id()
            order_item, status = OrderItem.objects.get_or_create(product=prod, ref_code=ref_code)
            user_order.items.add(order_item)
            user_order.ref_code = ref_code
            user_order.save()
        else:
            order_item, status = OrderItem.objects.get_or_create(product=prod, ref_code=user_order.ref_code)
            user_order.items.add(order_item)
            user_order.save()
        order_item.cost = order_item.qty * order_item.product.cost
        order_item.save()
        return render(request, 'marketplace/cart.html', {'order':user_order})
    else:
        prod = product.objects.get(id=id)
        user_order, status = Order.objects.get_or_create(user=request.user, is_ordered=False)
        order_item = OrderItem.objects.get(product=prod, ref_code=user_order.ref_code)
        order_item.cost = order_item.qty * order_item.product.cost
        order_item.save()
        return render(request, 'marketplace/cart.html', {'order':user_order})

def add_quantity(request, id):
    item = OrderItem.objects.get(pk=id)
    if item.qty < item.product.quantity:
        item.qty = item.qty + 1
        item.save()
    return redirect('/marketplace/add_to_cart/'+str(item.product.id))

def remove_quantity(request, id):
    item = OrderItem.objects.get(pk=id)
    item.qty = item.qty - 1
    item.save()
    return redirect('/marketplace/add_to_cart/'+str(item.product.id))

def delete(request, id):
    item = OrderItem.objects.get(pk=id)
    item.delete()
    return redirect('marketplace:products_blog')

@login_required()
def checkout(request, **kwargs):
    client_token = generate_client_token()
    existing_order = get_user_pending_order(request)
    if request.method == 'POST':
        result = transact({
            'amount': existing_order.get_cart_total(),
            'payment_method_nonce': request.POST['payment_method_nonce'],
            'options': {
                "submit_for_settlement": True
            }
        })

        if result.is_success or result.transaction:
            token= result.transaction.id
            # return redirect(reverse('marketplace:update_records',
            #         kwargs={
            #             'token': result.transaction.id
            #         })
            #     )
            order_to_purchase = get_user_pending_order(request)

            # update the placed order
            order_to_purchase.is_ordered=True
            order_to_purchase.date_ordered=datetime.datetime.now()
            order_to_purchase.save()

            # get all items in the order - generates a queryset
            order_items = order_to_purchase.items.all()

            # update order items
            order_items.update(is_ordered=True, date_ordered=datetime.datetime.now())



            # create a transaction
            transaction = Transaction(user=request.user,
                                    token=token,
                                    order_id=order_to_purchase.id,
                                    amount=order_to_purchase.get_cart_total(),
                                    success=True)
            # save the transcation (otherwise doesn't exist)
            transaction.save()


            messages.info(request, "Thank you! Your purchase was successful!")
            return HttpResponse("Saved")

        else:
            for x in result.errors.deep_errors:
                messages.info(request, x)
            return redirect(reverse('marketplace:checkout'))

    context = {
        'order': existing_order,
        'client_token': client_token,
    }
    return render(request, 'marketplace/checkout.html', context)

@login_required()
def update_transaction(request, token):
    # get the order being processed
    order_to_purchase = get_user_pending_order(request)

    # update the placed order
    order_to_purchase.is_ordered=True
    order_to_purchase.date_ordered=datetime.datetime.now()
    order_to_purchase.save()

    # get all items in the order - generates a queryset
    order_items = order_to_purchase.items.all()

    # update order items
    order_items.update(is_ordered=True, date_ordered=datetime.datetime.now())



    # create a transaction
    transaction = Transaction(user=request.user,
                            token=token,
                            order_id=order_to_purchase.id,
                            amount=order_to_purchase.get_cart_total(),
                            success=True)
    # save the transcation (otherwise doesn't exist)
    transaction.save()


    messages.info(request, "Thank you! Your purchase was successful!")
    return HttpResponse("Saved")

def add_tocart(request):
    return render(request, 'marketplace/cart.html')
