from rest_framework import serializers
from account.models import CustomUser
from .custom_errors import PlainValidationError
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator



class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model = CustomUser
        fields=['email','username','password','password2']
        extra_kwargs={
            'password':{'write_only':True}
        }


    # validating password and confirm password while registration
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if password != password2:
            raise PlainValidationError({'success': False,'message': 'password and confirm passwprd does not match'})

        return attrs

    def create(self, validate_data):
        return CustomUser.objects.create_user(**validate_data)

    
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = CustomUser
        fields = ['email','username', 'password']



class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username']


class UserChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length = 255,style = {'input_type':'password','write_only':True})
    password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only = True)
    password2 = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only = True)

    class Meta:
        fields = ['old_password','password', 'password2']

    def validate(self,attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        old_password = attrs.get('old_password')
        user = self.context.get('user')
        if password != password2:
            raise PlainValidationError({'success' : False, 'message': 'password and confirm password does not match' })

        elif old_password == password :
            raise PlainValidationError({'success': False,'message':'old password and new password should not be same'})

        user.set_password(password)
        user.save()
        return attrs


     #validate old password
    def validate_old_password(self, value):
        user = self.context.get('user')
        if not user.check_password(value):
            raise PlainValidationError({'success': False,'message':'old password is not correct'})
        return value


class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length = 255)

    class Meta:
        fields = ['email']


    def validate(self, attrs):
        email = attrs.get('email')

        if CustomUser.objects.filter(email=email).exists():
            user = CustomUser.objects.get(email = email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print(uid)
            print('Encoded UID', uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print('Password Reset Token', token)

            link = 'http://localhost:8000/api/user/reset-password/' + uid + '/' + token

            print('password reset link', link)

            return attrs

        else:
            raise PlainValidationError({'success': False,'message':'you are not a registered user'})



class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only = True)
    password2 = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only = True)

    class Meta:
        fields = ['password', 'password2']

    def validate(self,attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        uid = self.context.get('uid')
        token = self.context.get('token')
        
        user = self.context.get('user')
        if password != password2:
            raise PlainValidationError({'success' : False, 'message': 'password and confirm password does not match'})
        id = smart_str(urlsafe_base64_decode(uid))
        user = CustomUser.objects.get(id=id)

        if not PasswordResetTokenGenerator().check_token(user, token):
            raise PlainValidationError('Token is not valid or expired')
        user.set_password(password)
        user.save()
        return attrs


