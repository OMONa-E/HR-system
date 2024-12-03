from django.db import models
from applications.onboarding.models import Employee

# Attendance Model
# ----------------------------------
class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendance_logs')
    clock_in_time = models.DateTimeField()
    clock_out_time = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.employee.name} - {self.clock_in_time}'
    
    @property
    def duration(self):
        if self.clock_out_time:
            return self.clock_out_time - self.clock_in_time
        return None
