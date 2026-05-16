from django.urls import path
from .views import EventIngestView, DashboardSummaryView,TimeSeriesView

urlpatterns = [
    path('<slug:workspace_slug>/events/', EventIngestView.as_view(), name='event-ingest'),
    path('<slug:workspace_slug>/dashboard/summary/', DashboardSummaryView.as_view(), name='dashboard-summary'),
    path('<slug:workspace_slug>/dashboard/timeseries/', TimeSeriesView.as_view(), name='dashboard-timeseries'),
]