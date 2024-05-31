# views.py
from rest_framework import generics
from django.http import JsonResponse
from .models import Party,JoinParty
from .serializers import PartySerializer,JoinPartySerializer

class PartyDetailView(generics.RetrieveAPIView):
    queryset = Party.objects.all()
    serializer_class = PartySerializer

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Authentication required"}, status=401)

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return JsonResponse(serializer.data)

class PartyCreateView(generics.CreateAPIView):
    queryset = Party.objects.all()
    serializer_class = PartySerializer

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Authentication required"}, status=401)

        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        # Save the party and get the generated invite code
        new_party = serializer.save()
        generated_invite_code = new_party.invite_code

        return JsonResponse({"invite_code": generated_invite_code}, status=201)


class PartyUpdateView(generics.UpdateAPIView):
    queryset = Party.objects.all()
    serializer_class = PartySerializer

    def update(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Authentication required"}, status=401)

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return JsonResponse(serializer.data)
class GetOneView(generics.ListAPIView):
    queryset = Party.objects.all()
    serializer_class = PartySerializer

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Authentication required"}, status=401)

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
       # self.perform_update(serializer)
        return JsonResponse(serializer.data)
class UserPartyListView(generics.ListAPIView):
    serializer_class = PartySerializer

    def get_queryset(self):

        # Retrieve parties associated with the current user
        user = self.request.user
        return Party.objects.filter(user=user)

class PartyDeleteView(generics.DestroyAPIView):
    queryset = Party.objects.all()
    serializer_class = PartySerializer

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Authentication required"}, status=401)

        instance = self.get_object()
        self.perform_destroy(instance)
        return JsonResponse({"message": "Party deleted successfully"}, status=200)
class PartySearchView(generics.ListAPIView):
    serializer_class = PartySerializer

    def get_queryset(self):
        # if not request.user.is_authenticated:
        #     return JsonResponse({"error": "Authentication required"}, status=401)

        # Get the 'name' parameter from the query string
        name_query = self.request.query_params.get('name', '')

        # Filter parties by name (case-insensitive)
        parties = Party.objects.filter(name__icontains=name_query,public=True)
        return parties
class PartyByInviteCodeView(generics.RetrieveAPIView):
    queryset = Party.objects.all()
    serializer_class = PartySerializer
    lookup_field = 'invite_code'  # Use 'invite_code' as the lookup field

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return JsonResponse(serializer.data)
    
class JoinPartyCreateView(generics.CreateAPIView):
    queryset = JoinParty.objects.all()
    serializer_class = JoinPartySerializer

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Authentication required"}, status=401)

        # Automatically set the user field based on the logged-in user
        request.data['user'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return JsonResponse(serializer.data, status=201)
class JoinPartyUpdateView(generics.UpdateAPIView):
    queryset = JoinParty.objects.all()
    serializer_class = JoinPartySerializer
    def update(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Authentication required"}, status=401)

        return super().update(request, *args, **kwargs)

class JoinPartyDeleteView(generics.DestroyAPIView):
    queryset = JoinParty.objects.all()
    serializer_class = JoinPartySerializer
    def destroy(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Authentication required"}, status=401)

        return super().destroy(request, *args, **kwargs)


class JoinPartyByUserView(generics.ListAPIView):
    serializer_class = JoinPartySerializer

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return JsonResponse({"error": "Authentication required"}, status=401)
        user = self.request.user
        return JoinParty.objects.filter(user=user)

class JoinPartyByPartyView(generics.ListAPIView):
    serializer_class = JoinPartySerializer

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return JsonResponse({"error": "Authentication required"}, status=401)
        party_id = self.kwargs.get('party_id')
        return JoinParty.objects.filter(party_id=party_id)
