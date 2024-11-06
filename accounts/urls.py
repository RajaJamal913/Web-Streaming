from django.urls import path

from webapp import settings
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('register/', views.register_view, name='register'),  # User registration
    path('login/', views.login_view, name='login'),  # User login
    path('dashboard/', views.dashboard_view, name='dashboard'),  # Dashboard for logged-in users
    path('logout/', views.logout_view, name='logout'),  # Logout
    path('live-stream/', views.live_stream, name='live_stream'),  # Live stream page
    path('stop-stream/', views.stop_stream, name='stop_stream'),  # Stop stream and save the video

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

