from django.shortcuts import render, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from football.models import Player
from ..serializer import PlayerSerializer


# Create your views here.
class PlayerListView(generics.ListAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['club', 'position']
    ordering_fields = ['name', 'birth_date']       
    ordering = ['name']   

class PlayerDetailView(generics.RetrieveAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

def player_list_view(requests):
    players = Player.objects.all()
    return render(requests, 'api/player_list.html', {'players':players})



