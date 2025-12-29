from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from football.models import Player, Club
from .serializer import PlayerSerializer, ClubSerializer

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


class ClubListView(generics.ListAPIView):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['name', 'league', 'country']
    ordering_fields = ['name', 'league']
    ordering = ['name']
    

class ClubDetailView(generics.RetrieveAPIView):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer

def clubs_list_view(request):
    clubs = Club.objects.all()
    return render(request, 'api/club_list.html', {'clubs': clubs})

