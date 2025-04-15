from django.shortcuts import render, redirect, get_object_or_404
from .forms import SongUploadForm
from .models import Song, MyMusic
import subprocess
import os
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request, "home.html", {"user": request.user})

@login_required
def music_library(request):
    songs = Song.objects.all()
    return render(request, 'music_library.html', {'songs': songs})

@login_required
def upload_song(request):
    if request.method == 'POST':
        form = SongUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('music_library')
    else:
        form = SongUploadForm()
    return render(request, 'upload.html', {'form': form})

@login_required
def add_to_my_music(request, song_id):
    # Get the song using the provided song_id
    song = Song.objects.get(id=song_id)
    user = request.user  # Get the current logged-in user
    
    # Check if the user has already added this song to MyMusic
    if not MyMusic.objects.filter(user=user, song=song).exists():
        # Add the song to MyMusic for this user
        mymusic_entry = MyMusic(user=user, song=song)
        mymusic_entry.save()
        print(f"Song '{song.title}' added to {user.username}'s My Music.")
    else:
        print(f"Song '{song.title}' is already in {user.username}'s My Music.")
    
    # Redirect to the music library after adding
    return redirect('music_library')

# def player(request):
#     my_songs = MyMusic.objects.select_related('song').all()
#     return render(request, 'player.html', {'songs': my_songs})

@login_required
def player(request):
    if request.user.is_authenticated:
        my_music = MyMusic.objects.filter(user=request.user)
    else:
        my_music = None
    return render(request, "player.html", {"songs": my_music})

@login_required
def remove_from_my_music(request, song_id):
    # Ensure removal only occurs via POST (best practice)
    if request.method == "POST":
        my_music_entry = get_object_or_404(MyMusic, song__id=song_id)
        my_music_entry.delete()
    return redirect('player')

# GESTURE_SCRIPT_PATH = '/home/aadi/Documents/sixth_sem/projects/web_tech_project/web2/pyrunner/realtime_gesture_control.py'
# GESTURE_SCRIPT_PATH = '/tmp/test_gesture.py'
# PID_FILE = '/tmp/gesture_pid.txt'

# def toggle_gesture(request):
#     if os.path.exists(PID_FILE):
#         with open(PID_FILE, 'r') as f:
#             pid = int(f.read())
#         try:
#             os.kill(pid, 9)  # Kill the gesture process
#             os.remove(PID_FILE)
#         except ProcessLookupError:
#             pass
#     else:
#         process = subprocess.Popen(['python3', GESTURE_SCRIPT_PATH])
#         with open(PID_FILE, 'w') as f:
#             f.write(str(process.pid))

#     return redirect('player')

import signal

gesture_process = None  # Global process tracker

@login_required
def toggle_gesture(request):
    global gesture_process

    if request.method == 'POST':
        print("🔘 Gesture toggle button clicked!")

        try:
            if gesture_process and gesture_process.poll() is None:
                print("🛑 Gesture process is running. Terminating it...")
                gesture_process.terminate()
                gesture_process = None
                print("✅ Gesture process terminated.")
            else:
                print("▶️ Starting gesture script...")

                GESTURE_SCRIPT_PATH = '/home/aadi/Documents/sixth_sem/projects/web_tech_project/web2/pyrunner/realtime_gesture_control.py'

                gesture_process = subprocess.Popen(
                    ['python3', GESTURE_SCRIPT_PATH],
                    stdout=None,  # Send output to terminal
                    stderr=None,
                    preexec_fn=os.setsid
                )

                print(f"✅ Gesture script started with PID: {gesture_process.pid}")
        except Exception as e:
            print("❌ Error while toggling gesture script:", e)

    return redirect('player')

# def signup(request):
#     if request.method == "POST":
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("login")
#     else:
#         form = UserCreationForm()
#     return render(request, "signup.html", {"form": form})

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        print("POST data:", request.POST)
        if form.is_valid():
            form.save()
            print("User created successfully!")
            return redirect("login")
        else:
            print("Form errors:", form.errors)
    else:
        form = UserCreationForm()
    return render(request, "signup.html", {"form": form})