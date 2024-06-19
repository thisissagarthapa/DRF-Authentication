
from django.urls import path
from .views import *
urlpatterns = [
path('register/',UserRegistrationView.as_view(),name='register' ) , 
path('login/',UserLoginView.as_view(),name='login' ) ,  
path('user_profile/',UserProfileView.as_view(),name='user_profile' ) , 
path('changepassword/',UserChangePasswordView.as_view(),name='user_change_password' ) ,  
path('send-rest-password-email/',SendPasswordResetEmailView.as_view(),name='send-rest-password-email' ),
path('reset-password/<uid>/<token>/',UserResetPasswordView.as_view(),name='reset-password' )   
]
