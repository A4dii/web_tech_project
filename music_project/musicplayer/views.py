from django.shortcuts import render, redirect, get_object_or_404
from .forms import SongUploadForm
from .models import Song, MyMusic

def home(request):
    return render(request, 'home.html')

def music_library(request):
    songs = Song.objects.all()
    return render(request, 'music_library.html', {'songs': songs})

def upload_song(request):
    if request.method == 'POST':
        form = SongUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('music_library')
    else:
        form = SongUploadForm()
    return render(request, 'upload.html', {'form': form})

def add_to_my_music(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    if request.method == 'POST':
        if not MyMusic.objects.filter(song=song).exists():
            MyMusic.objects.create(song=song)
    return redirect('music_library')

def player(request):
    my_songs = MyMusic.objects.select_related('song').all()
    return render(request, 'player.html', {'songs': my_songs})

def remove_from_my_music(request, song_id):
    # Ensure removal only occurs via POST (best practice)
    if request.method == "POST":
        my_music_entry = get_object_or_404(MyMusic, song__id=song_id)
        my_music_entry.delete()
    return redirect('player')
