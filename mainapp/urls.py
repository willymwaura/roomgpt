from django.urls import path
from mainapp import views

urlpatterns = [
    path('',views.index,name='index'),
    path('dashboard',views.dashboard,name='dashboard'),
    
    path('login',views.login,name='login'),
    path('account',views.account,name='account'),
    path('create_account',views.create_account,name='create_account'),
    path('auth_login',views.auth_login,name='auth_login'),
    path('textimage',views.textimage,name='textimage'),
    path('imagetoimage',views.imagetoimage,name='imagetoimage'),
    path('checkout',views.checkout,name='checkout'),
    path('mpesa_checkout',views.mpesa_checkout,name='mpesa_checkout'),
    path('callback',views.PaymentCallback,name='callback')

]
