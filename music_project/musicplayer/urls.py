from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_song, name='upload'),
    path('player/', views.player, name='player'),
]
