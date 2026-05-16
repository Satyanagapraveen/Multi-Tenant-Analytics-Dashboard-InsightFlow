from django.db import models
from workspaces.models import Workspace

class Event(models.Model):
    workspace = models.ForeignKey(Workspace, related_name='events', on_delete=models.CASCADE)
    event_name = models.CharField(max_length=255)
    payload = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['workspace', 'created_at']),
            models.Index(fields=['workspace', 'event_name']),
        ]

    def __str__(self):
        return f"{self.event_name} - {self.workspace.slug}"