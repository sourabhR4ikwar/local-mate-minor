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
    ## forgot password
    ## Search
    path('search',views.search, name='search'),
    ## GuideProfile(Previous Trips, Reviews)
    path('guide/<int:guideid>', views.retrieveGuide, name='guide'),
    ## createTrip
    path('create-trip/<int:guideid>',views.createTrip, name='create-trip' ),
    path('create-trip-handler', views.createTripHandler, name='create-trip-handler'),
    path('payment/<int:tripId>', views.payment, name='payment'),
    path('payment-handler', views.paymentHandler, name='payment-handler'),
    ## Profile(Current and Previous Trips(Reviews and ratings))
    path('profile', views.profile, name='profile'),
    ## Conversation Page
    path('conversations', views.conversations, name='conversations'),
    path('send', views.send, name='send'),
]