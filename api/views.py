from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from football.models import Player, Club
from .serializer import PlayerSerializer

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

class PlayerCreateView(generics.CreateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

class PlayerUpdateView(generics.UpdateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

class PlayerDeleteView(generics.DestroyAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer  

def clubs_list_view(request):
    clubs = Club.objects.all()
    return render(request, 'api/club_list.html', {'clubs': clubs})

