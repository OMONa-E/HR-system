from rest_framework import serializers
from .models import LeaveRequest


# Leave Request Serializer
# ------------------------------------------------------------
class LeaveRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveRequest
        fields = '__all__'
        read_only_fields = [ 'status', 'created_at' ]
    