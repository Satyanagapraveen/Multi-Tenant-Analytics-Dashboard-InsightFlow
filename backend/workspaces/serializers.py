from rest_framework import serializers
from .models import Workspace

class WorkspaceSerializer(serializers.ModelSerializer):
    owner_email = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Workspace
        fields = ['id', 'name', 'slug', 'owner_email', 'created_at']
        read_only_fields = ['slug', 'created_at']