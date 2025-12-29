from django.urls import path
from .views import (
    PlayerListView,
    PlayerDetailView,
    clubs_list_view,
    ClubListView,
    ClubDetailView

)

urlpatterns = [
    path('players/', PlayerListView.as_view(), name='player-list'),
    path('players/<int:pk>/', PlayerDetailView.as_view(), name='player-detail'),
    

    path('clubs-web/', clubs_list_view, name='clubs-list-web'),
    path('clubs', ClubListView.as_view(), name='clubs_list'),
    path('clubs/<int:pk>/', ClubDetailView.as_view(), name='club-detail'),
]
