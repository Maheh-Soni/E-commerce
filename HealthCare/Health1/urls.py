from django.urls import path
from .views import *

urlpatterns = [
    path('',home,name="home"),
    path('shop/',shop,name="shop"),
    path('addcart/',addcart,name="addcart"),
    path('search/',search,name="search"),
    path('signup/',sign_up,name="signup"),
    path('login/',Log_in,name="login"),
    path('logout/',Log_out,name="logout"),
    path('add/<int:id>/',add,name="add"),
    path("item_payment/",item_payment,name='item_payment'),
    path("payment-Status/",payment_status,name='payment-status')
]
