from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('login/', views.login_view, name='login_view'),
    path('signup/', views.sigup_view, name='sigup_view'),
    path('signup_add/', views.signup_add, name='signup_add'),
   
]