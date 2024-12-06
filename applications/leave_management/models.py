from django.db import models
from applications.onboarding.models import Employee


# Leave Request Model
# ---------------------------------------
class LeaveRequest(models.Model):
    """
    Represents an employee's leave request.

    Attributes:
        employee (ForeignKey): Reference to the Employee model, indicating which employee made the leave request.
        start_date (DateField): The start date of the leave.
        end_date (DateField): The end date of the leave.
        reason (TextField): The reason for requesting leave.
        status (CharField): The status of the leave request, with choices:
            - 'Pending' (default): Leave request is awaiting review.
            - 'Approved': Leave request has been approved.
            - 'Rejected': Leave request has been rejected.
        created_at (DateTimeField): Timestamp indicating when the leave request was created.

    Methods:
        __str__(): Returns a string representation of the leave request, including the employee's name and the request status.
    """
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='leave_requests')
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.employee.full_name} - {self.status}'