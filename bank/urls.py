from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('payment/', views.payment_page, name='payment_page'),
    path('wallet/', views.wallet_page, name='wallet_page'),
    path('payment-category/', views.payment_category_page, name='payment_category_page'),
    path('login/', views.login_view, name='login_view'),
    path('signup/', views.signup_view, name='sigup_view'),
    path('logout/', views.logout_view, name='logout_view'),
]