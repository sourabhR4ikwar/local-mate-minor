from django.urls import path
from . import views


urlpatterns = [
    path('',views.homePage,name = 'home'),
    path('login',views.loginPage, name='login'),
    path('signup',views.signUpPage, name='signup'),
    path('loginHandler', views.loginProcess, name='loginProcess'),
    path('signUpHandler', views.signUpProcess, name='signUpProcess')
]