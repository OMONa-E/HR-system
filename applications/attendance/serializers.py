from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from .models import Attendance

# Attendance Serializer
# --------------------------------------------------------
class AttendanceSerializer(serializers.ModelSerializer):
    """
    Serializer for Attendance model.

    This serializer is responsible for serializing and deserializing Attendance 
    model instances, including fields such as employee, clock-in time, clock-out time, and 
    duration. The duration field is read-only and automatically calculated. 
    The employee field is a foriegn key

    Fields:
        id (int): Unique identifier for the attendance record.
        employee (int): Foreign key reference to the Employee model.
        clock_in_time (datetime): The date - time when the employee clocks in.
        clock_out_time (datetime): The date - time when the employee clocks out.
        duration (timedelta): Read-only field representing the duration 
                              between clock-in and clock-out times.
    """
    @extend_schema_field(serializers.CharField())
    def get_duration(self, obj):
        return str(obj.duration) if obj.duration else "Null"
    
    class Meta:
        model = Attendance
        fields = [ 'id', 'employee', 'clock_in_time', 'clock_out_time', 'duration' ]
        read_only_fields = [ 'duration' ]
