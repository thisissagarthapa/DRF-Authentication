from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .serializers import (UserRegistrationSerializer,
UserLoginSerialzer,UserProfileSerializer,UserChangePasswordSerializer
,SendPasswordResetEmailSerializer,UserPasswordResetSerializer)

from django.contrib.auth import authenticate
from .renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
class UserRegistrationView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,format=None):
        serializer=UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
            token=get_tokens_for_user(user)
            return Response({ 'token':token, 'msg':'registration success','status':status.HTTP_201_CREATED})
        return Response(serializer.errors,status=status.HTTP_401_UNAUTHORIZED)
    
    
class UserLoginView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,format=None):
        serializer=UserLoginSerialzer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email=serializer.data.get('email')
            password=serializer.data.get('password')
            user=authenticate(email=email,password=password)
            if user is not None:
                token=get_tokens_for_user(user)
                return Response({'token':token,'msg':'login successfully'},status=status.HTTP_200_OK)
            
            else:
                return Response({'errors':{'non field errors':['email or password is not valid']}},status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.error,status=status.HTTP_400_BAD_REQUEST)        

class UserProfileView(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]
    def get(self,request,fromat=None):
        serializer=UserProfileSerializer(request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)

class UserChangePasswordView(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]
    def post(self,request,format=None):
        serializer=UserChangePasswordSerializer(data=request.data,context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'password change successfully'},status=status.HTTP_200_OK)
        return Response(serializer.error,status=status.HTTP_404_NOT_FOUND)
            
            
class SendPasswordResetEmailView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,format=None):
        serializer=SendPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'password rest link sent.please check your mail'},status=status.HTTP_200_OK)
        return Response(serializer.error,status=status.HTTP_404_NOT_FOUND)

class UserResetPasswordView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,uid,token,format=None):
        serializer=UserPasswordResetSerializer(data=request.data,context={'uid':uid,'token':token})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'password reset successfully'},status=status.HTTP_200_OK)
        return Response(serializer.error,status=status.HTTP_404_NOT_FOUND)
