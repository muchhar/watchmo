from rest_framework import serializers
from account.models import User ,UserProfile
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
  
    class Meta:
        model =User
        fields=['email','password','password2']
        extra_kwargs={
      'password':{'write_only':True}
    }
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
        return attrs
    def create(self, validate_data):
        return User.objects.create_user(**validate_data)
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