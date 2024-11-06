from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import StreamingHttpResponse
import cv2


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

@login_required
def dashboard_view(request):
    return render (request, ('templates/dashboard.html'))

def logout_view(request):
    logout(request)
    return redirect('login')

def live_stream(request):
    # Initialize video capture for the laptop's default camera
    cap = cv2.VideoCapture(0)  # '0' refers to the default camera (e.g., laptop camera)
    return StreamingHttpResponse(generate_frames(cap), content_type='multipart/x-mixed-replace; boundary=frame')

def generate_frames(cap):
    while True:
        # Read the frame from the camera
        success, frame = cap.read()
        if not success:
            break
        # Encode the frame as JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        # Yield each frame as part of the response
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')