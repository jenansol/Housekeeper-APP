from django.shortcuts import render,redirect
import logging

logger = logging.getLogger(__name__)
#from django.contrib.auth.models import User
from .models import CustomUser
# from .models import User 

# Create your views here.
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken,TokenError
from django.contrib.auth import authenticate,login
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from .serializers import RegisterSerializercustomer, LoginSerializercustomer,RegisterSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, login
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status, generics
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.conf import settings
from .serializers import PasswordResetSerializer,PasswordResetConfirmSerializer,AdminPasswordResetSerializer, AdminPasswordResetConfirmSerializer
from django.core.mail import send_mail
from rest_framework.views import APIView


from django.contrib.auth import views as auth_views
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import get_user_model

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from .models import BlacklistedToken
from .utils import send_otp, verify_otp

import random
import requests
from django.core.cache import cache

User = get_user_model()


##################password Admin#####################################

class AdminPasswordResetView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = AdminPasswordResetSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Password reset token sent."})

class AdminPasswordResetConfirmView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = AdminPasswordResetConfirmSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Password has been reset."})





################Password Client########################
class PasswordResetView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PasswordResetSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.save()
        # Here you should send the token to the user's phone number via SMS
        return Response({"detail": "Password reset token sent."}, status=status.HTTP_200_OK)
    
    
class PasswordResetConfirmView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Password has been reset."}, status=status.HTTP_200_OK)


        
        
########################### clients views #########################################
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            phone_number = form.cleaned_data.get('phone_number')
           
            password = form.cleaned_data.get('password')
            user = authenticate(phone_number= phone_number, password=password)
            if user is not None:
                login(request, user)
                return redirect('/api/home')  # Redirect to home page
            else:
                return HttpResponse('Invalid login credentials')
        else:
            return HttpResponse('Invalid form data')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})



def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Redirect to home page
        else:
            return HttpResponse('Invalid form data')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# @login_required
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def home_view(request):
    return render(request, 'home.html')



class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializercustomer

    @swagger_auto_schema(
        request_body=RegisterSerializercustomer,
        responses={
            201: openapi.Response('User created successfully', RegisterSerializercustomer),
            400: "Bad Request"
        }
    )
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.validated_data
        phone_number = serializer.validated_data.get('phone_number')
        
        if send_otp(phone_number):
            return Response({"message": "OTP sent to phone number. Please verify to complete registration."}, status=status.HTTP_201_CREATED)
        
        else:
            return Response({
                'message': 'Failed to send OTP. Please try again later.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
     
        
class VerifyOTPView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')
        entered_otp = request.data.get('otp')

        if verify_otp(phone_number, entered_otp):
            # Proceed with registration confirmation logic
            return Response({
                'message': 'OTP verified successfully. Registration complete.'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'message': 'Invalid OTP. Please try again.'
            }, status=status.HTTP_400_BAD_REQUEST)

    
    
class LogoutView(APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'refresh_token': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['refresh_token']
        ),
        responses={
            200: "Logout successful",
            400: "Invalid token or no token provided",
        }
    )
    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get('refresh_token')
        if not refresh_token:
            return Response({'detail': 'No refresh token provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Decode and validate the refresh token
            token = RefreshToken(refresh_token)
            user_id = token.get('user_id')
            
             # Use the CustomUser model to check if the user exists
            if not CustomUser.objects.filter(id=user_id).exists():
                return Response({'detail': 'Invalid token or user does not exist'}, status=status.HTTP_400_BAD_REQUEST)

            # Check if the token is already blacklisted
            if BlacklistedToken.objects.filter(token=refresh_token).exists():
                return Response({'detail': 'Token is already blacklisted'}, status=status.HTTP_400_BAD_REQUEST)

            # Add the token to the blacklist
            BlacklistedToken.objects.create(token=refresh_token)
            return Response({'detail': 'Logout successful'}, status=status.HTTP_200_OK)
        except TokenError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    

    
    


class LoginView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializercustomer
    @swagger_auto_schema(
        request_body=LoginSerializercustomer,
        responses={
            200: openapi.Response('Login successful', openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'phone_number': openapi.Schema(type=openapi.TYPE_STRING),
                    'refresh': openapi.Schema(type=openapi.TYPE_STRING),
                    'access': openapi.Schema(type=openapi.TYPE_STRING),
                }
            )),
            400: "Invalid credentials"
        }
    )
    

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone_number']
        password = serializer.validated_data['password']
        # username= serializer.validated_data['']

        user = authenticate(request, phone_number=phone_number,  password=password, backend= 'login.backend.PhoneNumberBackend')

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'phone_number': user.phone_number,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            return Response({"detail": "Invalid credentials"}, status=400)
        
        
        
    ###########################################################################################################
    
        

    ############################################ system user ##################################################

class RegisterViewsystem(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    
    @swagger_auto_schema(
        request_body=RegisterSerializer,
        responses={
            201: openapi.Response('User created successfully', RegisterSerializer),
            400: "Bad Request"
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
   


class LoginViewsystem(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    
    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={
            200: openapi.Response('Login successful', openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'email': openapi.Schema(type=openapi.TYPE_STRING),
                    'refresh': openapi.Schema(type=openapi.TYPE_STRING),
                    'access': openapi.Schema(type=openapi.TYPE_STRING),
                    'is_staff': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    'is_superuser': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                }
            )),
            400: "Invalid credentials"
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        refresh = RefreshToken.for_user(user)
        return Response({
            'username':user.username,
            'email': user.email,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
            # 'role':user.role,
        })
    
    
class LogoutViewsystem(APIView):
    permission_classes = (AllowAny,)
    
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'refresh_token': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['refresh_token']
        ),
        responses={
            200: "Logout successful",
            400: "Invalid token or no token provided",
        }
    )
    
    

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data.get('refresh_token')
            if not refresh_token:
                return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
 
            # Decode the refresh token to get the user
            token = RefreshToken(refresh_token)
            user_id = token.get('user_id')
                
            if not User.objects.filter(id=user_id).exists():
                return Response({'detail': 'Invalid token or user does not exist'}, status=status.HTTP_400_BAD_REQUEST)

            # # Check if the token is already blacklisted
            #     if BlacklistedToken.objects.filter(token=refresh_token).exists():
            #         return Response({'detail': 'Token is already blacklisted'}, status=status.HTTP_400_BAD_REQUEST)

            # # Add the token to the blacklist
            #     BlacklistedToken.objects.create(token=refresh_token)
            return Response({'detail': 'Logout successful'}, status=status.HTTP_200_OK)
        except TokenError as e:
                return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
             

    

  
     
        
    