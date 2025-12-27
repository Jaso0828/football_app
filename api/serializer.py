from rest_framework import serializers
from football.models import Player

class PlayerSerializer(serializers.ModelSerializer):
    club_name = serializers.CharField(source='club.name', read_only=True)

    class Meta:
        model = Player
        fields = ['id', 'name', 'birth_date', 'position', 'club', 'club_name']    