from django.urls import path
from . import views


urlpatterns = [
    path('',views.homePage,name = 'home'),
    path('login',views.loginPage, name='login'),
    path('signup',views.signUpPage, name='signup'),
    path('signup-guide', views.signupGuidePage, name='signup_guide'),
    path('loginHandler', views.loginProcess, name='loginProcess'),
    path('signUpHandler', views.signUpProcess, name='signUpProcess'),
    path('signup-guide-handler', views.signupGuideProcess, name='signup_guide_process'),
]