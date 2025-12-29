from rest_framework import serializers
from football.models import Player, Club

class PlayerSerializer(serializers.ModelSerializer):
    player_name = serializers.CharField(source='player.name', read_only=True)

    class Meta:
        model = Player
        fields = ['id', 'name', 'birth_date', 'position', 'club', 'club_name']    

class ClubSerializer(serializers.ModelSerializer):
    club_name = serializers.CharField(source='club.name', read_only=True)

    class Meta:
        model = Club
        fields = '__all__'