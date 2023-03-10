from django.conf import settings
from django.core.mail import send_mail
import asyncio

def verification_mail(email ,  token):
    
    subject = 'Account verification'
    message = f'Hii , this is verification for your account http://127.0.0.1:3000/auth/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from,recipient_list)
    
    
    