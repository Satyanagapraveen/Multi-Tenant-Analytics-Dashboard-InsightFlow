from django.shortcuts import render
# Create your views here.
import os
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login, logout
from rest_framework.permissions import IsAuthenticated
from .models import User
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie

class GoogleLoginView(APIView):
    def post(self, request):
        code = request.data.get('code')
        if not code:
            return Response({'error': 'Code is required'}, status=status.HTTP_400_BAD_REQUEST)

        token_url = "https://oauth2.googleapis.com/token"
        token_data = {
            'code': code,
            'client_id': os.environ.get('GOOGLE_OAUTH2_CLIENT_ID'),
            'client_secret': os.environ.get('GOOGLE_OAUTH2_CLIENT_SECRET'),
            'redirect_uri':'postmessage',
            'grant_type': 'authorization_code',
        }
        
        token_res = requests.post(token_url, data=token_data)
        if not token_res.ok:
            return Response({'error': 'Failed to exchange token with Google'}, status=status.HTTP_400_BAD_REQUEST)

        access_token = token_res.json().get('access_token')

        user_info_url = "https://www.googleapis.com/oauth2/v1/userinfo"
        user_res = requests.get(user_info_url, headers={'Authorization': f'Bearer {access_token}'})
        
        if not user_res.ok:
            return Response({'error': 'Failed to fetch user profile'}, status=status.HTTP_400_BAD_REQUEST)

        user_data = user_res.json()
        email = user_data.get('email')

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'username': email.split('@')[0], 
                'name': user_data.get('name', ''),
                'avatar_url': user_data.get('picture', ''),
                'provider': 'google',
                'provider_user_id': user_data.get('id', '')
            }
        )

        login(request, user)

        return Response({
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'avatar_url': user.avatar_url
        })
@method_decorator(ensure_csrf_cookie, name='dispatch')
class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            'id': request.user.id,
            'email': request.user.email,
            'name': request.user.name,
            'avatar_url': request.user.avatar_url
        })
