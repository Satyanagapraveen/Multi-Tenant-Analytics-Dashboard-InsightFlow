from django.urls import path
from .views import EventIngestView

urlpatterns = [
    path('<slug:workspace_slug>/events/', EventIngestView.as_view(), name='event-ingest'),
]