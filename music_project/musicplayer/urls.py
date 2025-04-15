from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_song, name='upload'),
    path('player/', views.player, name='player'),
    path('library/', views.music_library, name='music_library'),
    path('add-to-my-music/<int:song_id>/', views.add_to_my_music, name='add_to_my_music'),
    path('remove-from-my-music/<int:song_id>/', views.remove_from_my_music, name='remove_from_my_music'),
]
