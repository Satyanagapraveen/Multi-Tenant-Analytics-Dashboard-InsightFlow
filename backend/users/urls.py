from django.urls import path
from .views import GoogleLoginView, CurrentUserView

urlpatterns = [
    path('auth/google/', GoogleLoginView.as_view(), name='google-login'),
    path('auth/me/', CurrentUserView.as_view(), name='current-user'),
]