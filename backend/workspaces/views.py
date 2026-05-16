from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.utils.text import slugify
from .models import Workspace, WorkspaceMembership
from .serializers import WorkspaceSerializer

class WorkspaceListCreateView(generics.ListCreateAPIView):
    serializer_class = WorkspaceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Workspace.objects.filter(workspacemembership__user=self.request.user)

    def perform_create(self, serializer):
        base_slug = slugify(serializer.validated_data['name'])
        slug = base_slug
        counter = 1
        
        while Workspace.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        workspace = serializer.save(owner=self.request.user, slug=slug)
        WorkspaceMembership.objects.create(
            user=self.request.user, 
            workspace=workspace, 
            role='admin'
        )