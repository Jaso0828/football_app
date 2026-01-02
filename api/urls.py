from django.urls import path
from .views.club_views import (club_detail_view,
                              clubs_list_view,
                              ClubDetailView,
                              ClubListView)
from .views.player_views import(PlayerListView,
                               PlayerDetailView,
                               player_list_view)


urlpatterns = [
    #API
    path('api/players/', PlayerListView.as_view(), name='player-list-api'),
    path('api/players/<int:pk>/', PlayerDetailView.as_view(), name='player-detail-api'),

    path('api/clubs/', ClubListView.as_view(), name='clubs_list_api'),
    path('api/clubs/<int:pk>/', ClubDetailView.as_view(), name='club_detail_api'),

    #HTML.  
    path('', clubs_list_view, name='clubs'),
    path('clubs/<int:pk>/', club_detail_view, name='club-detail'),
    path('players/', player_list_view, name='players'),
]
