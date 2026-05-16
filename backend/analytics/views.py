from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated,AllowAny 
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from workspaces.models import Workspace, WorkspaceMembership
from .models import Event
from .serializers import EventSerializer
from rest_framework.views import APIView 
from rest_framework.response import Response
from django.db.models import Count
from django.core.cache import cache
from django.db.models.functions import TruncDate
from django.utils import timezone
from datetime import timedelta

@method_decorator(csrf_exempt, name='dispatch')
class EventIngestView(generics.CreateAPIView):
    serializer_class = EventSerializer
    permission_classes = [AllowAny] # Unlocked!

    def perform_create(self, serializer):
        # 1. Grab the slug from the URL
        workspace_slug = self.kwargs.get('workspace_slug')
        
        # 2. Find the workspace (crashes with 404 if someone tries a fake slug)
        workspace = get_object_or_404(Workspace, slug=workspace_slug)

        # 3. Save the event directly. No user checks required!
        serializer.save(workspace=workspace)

    def perform_create(self, serializer):
        workspace_slug = self.kwargs.get('workspace_slug')
        workspace = get_object_or_404(Workspace, slug=workspace_slug)

        is_member = WorkspaceMembership.objects.filter(
            user=self.request.user,
            workspace=workspace
        ).exists()

        if not is_member:
            raise PermissionDenied("You do not have access to this workspace.")

        serializer.save(workspace=workspace)

class DashboardSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, workspace_slug):
        workspace = get_object_or_404(Workspace, slug=workspace_slug)

        is_member = WorkspaceMembership.objects.filter(
            user=request.user,
            workspace=workspace
        ).exists()

        if not is_member:
            raise PermissionDenied("You do not have access to this workspace.")

        # --- NEW CACHING LOGIC STARTS HERE ---
        cache_key = f"workspace_{workspace.id}_dashboard_summary"
        cached_data = cache.get(cache_key)

        if cached_data:
            print("CACHE HIT! Serving from Redis RAM.")
            return Response(cached_data)

        print("CACHE MISS! Calculating in Postgres.")
        
        # --- ORIGINAL QUERY LOGIC ---
        total_events = Event.objects.filter(workspace=workspace).count()

        events_by_type = (
            Event.objects.filter(workspace=workspace)
            .values('event_name')
            .annotate(count=Count('id'))
            .order_by('-count')
        )

        data = {
            "total_events": total_events,
            "events_by_type": list(events_by_type)
        }

        # --- STORE RESULT IN REDIS ---
        cache.set(cache_key, data, timeout=60*15)

        return Response(data)
    

class TimeSeriesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, workspace_slug):
        workspace = get_object_or_404(Workspace, slug=workspace_slug)

        is_member = WorkspaceMembership.objects.filter(
            user=request.user,
            workspace=workspace
        ).exists()

        if not is_member:
            raise PermissionDenied("You do not have access to this workspace.")

        period = request.query_params.get('period', '7d')
        days = int(period.replace('d', ''))
        start_date = timezone.now() - timedelta(days=days)

        timeseries_data = (
            Event.objects.filter(workspace=workspace, created_at__gte=start_date)
            .annotate(date=TruncDate('created_at'))
            .values('date')
            .annotate(count=Count('id'))
            .order_by('date')
        )

        return Response(list(timeseries_data))