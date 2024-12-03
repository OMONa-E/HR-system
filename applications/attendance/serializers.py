from rest_framework import serializers
from .models import Attendance

# Attendance Serializer
# --------------------------------------------------------
class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = [ 'id', 'employee', 'clock_in_time', 'clock_out_time', 'duration' ]
        read_only_fields = [ 'duration' ]
