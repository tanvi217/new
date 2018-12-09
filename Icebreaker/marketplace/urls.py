from django.urls import path
from django.conf.urls import url
from . import views

app_name='marketplace'

urlpatterns = [
    url(r'^blog/$',views.products_all, name="products_blog"),
    url(r'^(?P<slug>[0-9]+)/$', views.product_details, name="product_details"),
    url(r'^my_products/$', views.my_products, name="my_products"),
    url(r'^add/$',views.add_product, name="add_product"),
    url(r'edit_product/(?P<id>\d+)/$', views.edit_product, name="edit_product"),
    url(r'del_product/(?P<id>\d+)/$', views.delete_product, name="delete_product"),

]
