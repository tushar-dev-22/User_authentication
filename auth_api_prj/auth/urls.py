from django.urls import path
from .views import SignUpView,SignInView , Verification , UserVerify

urlpatterns = [
    
    path('sign-up/', SignUpView.as_view() , name="sign-up"),
    path('sign-in/', SignInView.as_view() , name="sign-in"),
    path('sign-in/', SignInView.as_view() , name="sign-in"),
    path('email-verifiaction/', Verification.as_view() , name= 'email-verification'),
    path('verify/<auth_token>', UserVerify.as_view() , name= 'user-verify')
]
