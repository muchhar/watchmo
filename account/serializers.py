from rest_framework import serializers
from account.models import User ,UserProfile
import random
import string

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
  
    class Meta:
        model = User
        fields = ['email', 'password', 'password2']
        extra_kwargs = {'password': {'write_only': True}}
    
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        
        # Create UserProfile with default values if not provided
        default_username = 'user' + ''.join(random.choices(string.digits, k=3))
        default_user_icon = 'user_icons/fvc.png'
        
        UserProfile.objects.create(
            user=user,
            username=default_username,
            user_icon=default_user_icon
        )
        
        return user
class UserLoginSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(max_length=255)
  class Meta:
    model = User
    fields = ['email', 'password']
class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), default=serializers.CurrentUserDefault())

    class Meta:
        model = UserProfile
        fields = ['user', 'username', 'user_icon']

    def update(self, instance, validated_data):
        # Update existing user profile
        instance.username = validated_data.get('username', instance.username)
        instance.user_icon = validated_data.get('user_icon', instance.user_icon)
        instance.save()
        return instance
class UserProfileRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username', 'user_icon']
