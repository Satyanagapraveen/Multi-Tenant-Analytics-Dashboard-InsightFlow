from django.urls import path
from .views import GoogleLoginView, CurrentUserView,LogoutView

urlpatterns = [
    path('auth/google/', GoogleLoginView.as_view(), name='google-login'),
    path('auth/me/', CurrentUserView.as_view(), name='current-user'),
    path('auth/logout',LogoutView.as_view(),name='logout')
]