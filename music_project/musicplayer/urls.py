from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect("login"), name='root'),
    path("home/", views.home, name="home"),
    path('upload/', views.upload_song, name='upload'),
    path('player/', views.player, name='player'),
    path('library/', views.music_library, name='music_library'),
    path('add-to-my-music/<int:song_id>/', views.add_to_my_music, name='add_to_my_music'),
    path('remove-from-my-music/<int:song_id>/', views.remove_from_my_music, name='remove_from_my_music'),
    path('toggle-gesture/', views.toggle_gesture, name='toggle_gesture'),
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="home"), name="logout"),
    path("signup/", views.signup, name="signup"),
]
