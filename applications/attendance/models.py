from django.db import models
from applications.onboarding.models import Employee

# Attendance Model
# ----------------------------------
class Attendance(models.Model):
    """
    Represents an employee's attendance log.

    This model stores clock-in and clock-out times for employees, allowing 
    calculation of the duration of attendance.

    Attributes:
        employee (ForeignKey): A reference to the Employee model, indicating which employee the log belongs to.
        clock_in_time (DateTimeField): The date and time when the employee clocked in.
        clock_out_time (DateTimeField, optional): The date and time when the employee clocked out.
                                                 Can be null if the employee has not clocked out yet.

    Methods:
        __str__(): Returns a string representation of the attendance log, 
                   including the employee's name and clock-in time.
        duration (timedelta): A property that calculates the duration between 
                              clock-in and clock-out times. Returns None if the 
                              clock-out time is not set.
    """
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendance_logs')
    clock_in_time = models.DateTimeField()
    clock_out_time = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.employee.name} - {self.clock_in_time}'
    
    @property
    def duration(self):
        """
        Calculates the duration between clock-in and clock-out times.

        Returns:
            timedelta: The time difference between clock-out and clock-in if 
                       clock-out time is set.
            None: If the clock-out time is not set.
        """
        if self.clock_out_time:
            return self.clock_out_time - self.clock_in_time
        return None
