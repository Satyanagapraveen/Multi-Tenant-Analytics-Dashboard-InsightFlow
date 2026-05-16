from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from workspaces.models import Workspace, WorkspaceMembership
from .models import Event
from .serializers import EventSerializer
from rest_framework.views import APIView 
from rest_framework.response import Response
from django.db.models import Count

class EventIngestView(generics.CreateAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

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

        total_events = Event.objects.filter(workspace=workspace).count()

        events_by_type = (
            Event.objects.filter(workspace=workspace)
            .values('event_name')
            .annotate(count=Count('id'))
            .order_by('-count')
        )

        return Response({
            "total_events": total_events,
            "events_by_type": list(events_by_type)
        })