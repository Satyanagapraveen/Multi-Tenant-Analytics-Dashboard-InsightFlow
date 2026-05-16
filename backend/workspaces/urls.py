from .views import WorkspaceListCreateView
from django.urls import path
urlpatterns = [
    path('',WorkspaceListCreateView.as_view(),name='workspace-list'),
]
