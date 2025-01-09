from django.urls import path
from .views import SongListView, SongUploadView, SongDeleteView

urlpatterns = [
    path('songs/', SongListView.as_view(), name='song-list'),
    path('upload/', SongUploadView.as_view(), name='song-upload'),
    path('songs/<int:song_id>/', SongDeleteView.as_view(), name='song-delete'),
    
    ]
