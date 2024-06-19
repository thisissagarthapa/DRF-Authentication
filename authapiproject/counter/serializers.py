from rest_framework import serializers
from .models import User
from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import Util
class UserRegistrationSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={'input_type':'password'},write_only=True)
    class  Meta:
        
        model=User
        fields=['email','name','password','password2','tc']
        extra_kwargs={
            'password':{'write_only':True}
            
        }
        
    def validate(self,attrs):
        password=attrs.get('password')
        password2=attrs.get('password2')
        if password!=password2:
            raise serializers.ValidationError("password and confirmaton doesn't match")
        return attrs
        
    def create(self,validate_data):
        return User.objects.create_user(**validate_data)

class UserLoginSerialzer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255)
    class  Meta:
        model=User
        fields=['email','password']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','name','email']
     
class UserChangePasswordSerializer(serializers.Serializer):
    
    password=serializers.CharField(max_length=255,style={'input type':'password'},write_only=True)  
    password2=serializers.CharField(max_length=255,style={'input type':'password'},write_only=True)  
      
    class Meta:
        model=User
        fields=['password','password2']
    
    def validate(self, attrs):
        password=attrs.get('password')
        password2=attrs.get('password2')
        user=self.context.get('user')
        if password!=password2:
            raise serializers.ValidationError("password  and password2 doesn't match")
        user.set_password(password)
        user.save()
        return attrs
        
        
class SendPasswordResetEmailSerializer(serializers.Serializer):
    email=serializers.EmailField(max_length=255)
    class  Meta:
        model=User
        fields=['email']
    def validate(self, attrs):
        email=attrs.get('email')
        if User.objects.filter(email=email).exists():
            user=User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print('Encoded id :',uid)
            token=PasswordResetTokenGenerator().make_token(user)
            link='https:/localhost:3000/api/user/reset/'+uid+'/'+token
            print('password Reset Link',link)
            print('Password Reset Token:',token)
            #Send email
            body='Click following link to reset your password'+link
            data={
                'email_subject':'reset your password',
                'body':body,
                'to_email':user.email
            }
            Util.send_email(data)
            return attrs
        else:
            raise serializers.ValidationError('you are not a registered user')



class UserPasswordResetSerializer(serializers.Serializer):
    password=serializers.CharField(max_length=255,style={'input type':'password'},write_only=True)  
    password2=serializers.CharField(max_length=255,style={'input type':'password'},write_only=True)  
      
    class Meta:
        model=User
        fields=['password','password2']
    
    def validate(self, attrs):
        try:
            password=attrs.get('password')
            password2=attrs.get('password2')
            uid=self.context.get('uid')
            token=self.context.get('token')
            if password!=password2:
                raise serializers.ValidationError("password  and password2 doesn't match")
            id= smart_str(urlsafe_base64_decode(uid))
            user=User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user,token):
                raise serializers.ValidationError('Token is not valid or expired')
            user.set_password(password)
            user.save()
            
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user,token)
            raise serializers.ValidationError('Token is not valid or expired')