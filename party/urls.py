# urls.py
from django.urls import path
from .views import *
urlpatterns = [
    path('create/', PartyCreateView.as_view(), name='party-create'),
    path('update/<int:pk>/', PartyUpdateView.as_view(), name='party-update'),
    path('get/all/', UserPartyListView.as_view(), name='user-party-list'),
    path('delete/<int:pk>/', PartyDeleteView.as_view(), name='party-delete'),
    path('get/<int:pk>/', PartyDetailView.as_view(), name='party-detail'),  # New endpoint for getting party by ID
    
    #path('get/<int:pk>/',GetOneView.as_view(),name='get-one'),
    path('search/', PartySearchView.as_view(), name='party-search'),
    
    
    path('by_invite_code/<str:invite_code>/', PartyByInviteCodeView.as_view(), name='party-by-invite-code'),
    
    path('joinparty/submit/', JoinPartyCreateView.as_view(), name='joinparty-create'),
    path('joinparty/update/<int:pk>/', JoinPartyUpdateView.as_view(), name='joinparty-update'),
    path('joinparty/delete/<int:pk>/', JoinPartyDeleteView.as_view(), name='joinparty-delete'),
    
    path('joinparty/by_user/', JoinPartyByUserView.as_view(), name='joinparty-by-user'),
    path('joinparty/by_party/<str:party_id>/', JoinPartyByPartyView.as_view(), name='joinparty-by-party'),
   
    
    # Add other URL patterns as needed
]
