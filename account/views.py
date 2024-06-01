from rest_framework.response import Response
from rest_framework import status,generics
from rest_framework.views import APIView
from account.serializers import UserRegistrationSerializer,UserLoginSerializer ,UserProfileSerializer,UserProfileRetrieveSerializer,UserSerializer
from .models import UserProfile
from django.contrib.auth import authenticate
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.apple.views import AppleOAuth2Adapter
from allauth.socialaccount.helpers import complete_social_login

from rest_framework_simplejwt.tokens import RefreshToken, BlacklistMixin
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework.generics import RetrieveAPIView

def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }

class UserDetailView(RetrieveAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileRetrieveSerializer
    permission_classes = [AllowAny]
    lookup_field = 'user__id'

    def get(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        try:
            user_profile = UserProfile.objects.get(user__id=user_id)
            serializer = self.get_serializer(user_profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
class SocialLoginView(APIView):
    def post(self, request, *args, **kwargs):
        adapter_class = None
        if 'google' in request.data.get('provider', ''):
            adapter_class = GoogleOAuth2Adapter
        elif 'apple' in request.data.get('provider', ''):
            adapter_class = AppleOAuth2Adapter

        if adapter_class:
            adapter = adapter_class()
            user, auth = complete_social_login(request, adapter)
            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)

        return Response({"error": "Invalid social provider"}, status=status.HTTP_400_BAD_REQUEST)

class UserRegistrationView(APIView):
    def post(self,request,format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'token':token, 'msg':'Registration Successful'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
  
  def post(self, request, format=None):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            token = get_tokens_for_user(user)
            return Response({'token':token, 'msg':'Login Success'}, status=status.HTTP_200_OK)
        else:
            return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
class UserProfileCreateUpdateView(generics.CreateAPIView, generics.UpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Get or create user profile based on the authenticated user
        user = self.request.user
        obj, created = UserProfile.objects.get_or_create(user=user)
        return obj
class UserProfileRetrieveView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Get the user profile based on the authenticated user
        user_profile = UserProfile.objects.get(user=self.request.user)
        return user_profile
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Revoke the refresh token
        refresh_token = request.data.get('refresh_token')
        if not refresh_token:
            return Response({'detail': 'Refresh token not provided.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            BlacklistMixin.blacklist(RefreshToken(refresh_token))
        except Exception as e:
            return Response({'detail': 'Error revoking token.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'detail': 'Logout successful.'}, status=status.HTTP_200_OK)
