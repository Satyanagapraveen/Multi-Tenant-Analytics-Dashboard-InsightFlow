from django.urls import path
from .views import EventIngestView, DashboardSummaryView

urlpatterns = [
    path('<slug:workspace_slug>/events/', EventIngestView.as_view(), name='event-ingest'),
    path('<slug:workspace_slug>/dashboard/summary/', DashboardSummaryView.as_view(), name='dashboard-summary'),
]