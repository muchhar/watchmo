# serializers.py
from rest_framework import serializers
from .models import Party,JoinParty

class PartySerializer(serializers.ModelSerializer):
    class Meta:
        model = Party
        exclude = ['invite_code', 'user']  # Exclude fields during creation


    def create(self, validated_data):
        # Get the user from the context (passed from the view)
        user = self.context['request'].user

        # Add the user to the validated data before creating the party
        validated_data['user'] = user

        # Call the default create method to create the party
        party = super(PartySerializer, self).create(validated_data)

        return party
class JoinPartySerializer(serializers.ModelSerializer):
    class Meta:
        model = JoinParty
        fields = ['id','user', 'party_id', 'data']
