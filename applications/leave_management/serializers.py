from rest_framework import serializers
from .models import LeaveRequest


# Leave Request Serializer
# ------------------------------------------------------------
class LeaveRequestSerializer(serializers.ModelSerializer):
    """
    Serializer for the LeaveRequest model.

    This serializer handles the serialization and deserialization of LeaveRequest 
    objects for use in API views. Fields such as 'status' and 'created_at' are read-only.

    Meta:
        model (LeaveRequest): The model being serialized.
        fields ('__all__'): All fields from the LeaveRequest model are included.
        read_only_fields (list): 
            - status: The status of the leave request is set as 'Pending' by default 
                      and can only be updated by specific endpoints.
            - created_at: The creation timestamp is automatically generated and not editable.
    """
    class Meta:
        model = LeaveRequest
        fields = '__all__'
        read_only_fields = [ 'status', 'created_at' ]
    