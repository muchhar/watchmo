
from django.urls import path,include
from account.views import *
urlpatterns = [
    path('register/',UserRegistrationView.as_view(),name='register'),
    path('login/',UserLoginView.as_view(),name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    path('user-profile/', UserProfileCreateUpdateView.as_view(), name='user-profile'),
    path('retrieve-profile/', UserProfileRetrieveView.as_view(), name='retrieve-profile'),
    
    path('api/social/login/', SocialLoginView.as_view(), name='social-login'),

]
