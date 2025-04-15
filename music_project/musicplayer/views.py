from django.shortcuts import render, redirect
from .forms import SongForm
from .models import Song

def home(request):
    return render(request, 'home.html')

def upload_song(request):
    if request.method == 'POST':
        form = SongForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('player')
    else:
        form = SongForm()
    return render(request, 'upload.html', {'form': form})

def player(request):
    songs = Song.objects.all()
    return render(request, 'player.html', {'songs': songs})
