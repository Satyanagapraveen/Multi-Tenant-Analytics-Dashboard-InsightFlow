from django.contrib import admin
from .models import Workspace, WorkspaceMembership

@admin.register(Workspace)
class WorkspaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'owner', 'created_at')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(WorkspaceMembership)
class WorkspaceMembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'workspace', 'role', 'joined_at')
    list_filter = ('role', 'workspace')