from django.urls import path
from . import views

app_name = 'polls'
urlpatterns = [

    path('', views.index, name='index'),

    path('polls/<int:qid>/', views.detail, name='detail'),

    path('query/', views.query_view, name='query_view'),

    path('adminpage/', views.adminpage, name='adminpage'),

    #path('result/',views.result,name='result'),

   # path('sendmail/', views.sendmail, name='sendmail'),



]