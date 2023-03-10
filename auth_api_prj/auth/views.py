from django.http import JsonResponse
from django.shortcuts import render,redirect , HttpResponse
from account.models import CustomUser , EmailVerificationToken
from django.conf import settings
from django.views import View
from django.contrib import messages
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate , login
from django.contrib.auth.decorators import user_passes_test
import re
from django.middleware.csrf import get_token
from django.utils.decorators import method_decorator
from django.contrib.sites.shortcuts import get_current_site
import json
import uuid
from .helpers import verification_mail

# Create your views here.

APP_THEME =  settings.APP_THEME


#Check if user is not logged in
def not_logged_in(user):
    return not user.is_authenticated

# User Signup view
class SignUpView(View):
    
    @method_decorator(user_passes_test(not_logged_in, login_url='/dashboard/home-dashboard'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request,*args, **kwargs):
        context = {
            
            'APP_THEME': APP_THEME
        }
        return render(request,'_templates/'+APP_THEME+'pages/accounts/signup.html', context)
    
    def post(self , request,*args, **kwargs):
            
        try:
            if request.method == 'POST':
                
                email = request.POST.get('email')
                username = request.POST.get('username')
                first_name =  request.POST.get('first_name')
                last_name = request.POST.get('last_name')
                phone_number = request.POST.get('phone_number')
                password = request.POST.get('password')
                confirm_password = request.POST.get('confirm_password')
                
                pattern = re.compile("^\+[1-9]\d{1,2}")
                auth_token = str(uuid.uuid4())
                #Validation check:
                if CustomUser.objects.filter(email=email).exists():
                    return JsonResponse({
                        
                        'status' : 400,
                        'message': 'This email address already exists. Please try with a different email',
                        'data' :   None
                        
                        })

                if password != confirm_password:
                    return JsonResponse({
                        
                        'status' : 401,
                        'message': "Password and confirm password does not match",
                        'data' :   None
                        
                        })
                
                if not pattern.match(phone_number):
                    return JsonResponse({
                        
                        'status' : 402,
                        'message': 'Phone number is invalid',
                        'data' :   None
                        
                        })
                
                data = CustomUser.objects.create_user(email=email,username=username,first_name=first_name,last_name=last_name,phone_number=phone_number,password=password)
                user_verify = EmailVerificationToken.objects.create(user=data , auth_token = auth_token)
                user_verify.save()
                verification_mail(email , auth_token)
                return JsonResponse({
                    
                    'status' : 200,
                    'success': True,
                    'message' : 'User has been successfully registered',
                    'redirect':'http://'+get_current_site(request).domain+'/auth/email-verifiaction/' })
                
        except:       
            return JsonResponse({'message': 'Invalid request'})
        
class Verification(View):
    
    def get(self , request , *args, **kwargs):
        context = {
            
            'APP_THEME': APP_THEME
        }
        return render(request,'_templates/'+APP_THEME+'pages/accounts/verification.html', context)
    
#User email verification view
class UserVerify(View):
    
        def get(self , request , auth_token):
            try:
                user_verify = EmailVerificationToken.objects.filter(auth_token=auth_token).first()
                if user_verify is not None:
                    user_verify.is_verified = True
                    user_verify.save()
                    user = user_verify.user
                    user.is_email_verified = True
                    user.save()
                    return redirect('/auth/sign-in/')
            except Exception as e:
                print(e)        
                return redirect('/auth/error/')

# User login view
class SignInView(View):
    @method_decorator(user_passes_test(not_logged_in, login_url='/dashboard/home-dashboard'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request,*args, **kwargs):
        context = {
            
            'APP_THEME': APP_THEME,
        }
        return render(request,'_templates/'+APP_THEME+'pages/accounts/login.html', context)
    
    def post(self,request , *args, **kwargs):
        try:
            if request.method == 'POST':
                
                username = request.POST.get('username')
                password = request.POST.get('password')
                user = authenticate(request, username = username ,password=password)

                if user is not None :
                    if not user.is_email_verified:
                        return JsonResponse({
                            'status': 401,
                            'message': 'Your email is not verified',
                            'data': {
                                'redirect': 'http://' + get_current_site(request).domain + '/auth/sign-in/'
                            }
                        })
                    else:
                        login(request,user)
                        return JsonResponse({
                            'status':200,
                            'message': 'User has been logged in successfully.',
                            'data':{
                                'redirect':'http://'+get_current_site(request).domain+'/dashboard/home-dashboard/'
                            }
                        })
                else:
                    return JsonResponse({
                        'status':400,
                        'message' : 'Authentication failed. Please try again with valid credentials!',
                        'data' : {}
                    })
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'Invalid request'})
