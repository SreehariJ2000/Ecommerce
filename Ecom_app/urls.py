from django.urls import path
from Ecom_app import views

urlpatterns=[
path('',views.index,name='index')

]