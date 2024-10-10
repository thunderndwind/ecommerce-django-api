from django.urls import path
from .views import UserRegistrationView, FaceIDLoginView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', FaceIDLoginView.as_view(), name='face_login'),
]
