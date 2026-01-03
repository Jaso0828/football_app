from django.shortcuts import render, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from football.models import  Club, Player
from ..serializer import ClubSerializer




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


def club_detail_view(request, pk):
    club = get_object_or_404(Club, pk=pk)
    players = club.players.all()
    return render(request, 'api/club_detail.html', {'club': club, 'players': players})


