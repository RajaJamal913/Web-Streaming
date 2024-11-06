from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from accounts.models import VideoRecording
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, StreamingHttpResponse
import cv2
from datetime import datetime

# User registration view
def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "Registration successful. Please log in.")
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'templates/register.html', {'form': form})

# Login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Change 'dashboard' to your dashboard URL name
        else:
            messages.error(request, "Invalid credentials.")
    return render(request, 'templates/login.html')

# Dashboard view
@login_required
def dashboard_view(request):
    # Retrieve all recorded videos for the current user
    videos = VideoRecording.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'videos': videos})

# Logout view
def logout_view(request):
    logout(request)
    return redirect('login')

# Function to serve the live stream feed
def live_stream(request):
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    return StreamingHttpResponse(generate_frames(cap), content_type='multipart/x-mixed-replace; boundary=frame')

# Function to generate frames for live streaming and recording
def generate_frames(cap):
    # Define codec and create VideoWriter for saving the video
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    filename = f"media/video_recordings/{datetime.now().strftime('%Y%m%d_%H%M%S')}.avi"
    out = cv2.VideoWriter(filename, fourcc, 20.0, (640, 480))  # 20 FPS, 640x480 resolution

    while True:
        success, frame = cap.read()
        if not success:
            break

        # Write frame to the output video file
        out.write(frame)

        # Encode frame as JPEG for streaming
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()
    out.release()

# Function to stop the stream and save the recording
def stop_stream(request):
    # The stream should be saved automatically when `generate_frames` finishes
    # You can add additional cleanup or database operations here
    return HttpResponse('Stream recorded successfully!')

