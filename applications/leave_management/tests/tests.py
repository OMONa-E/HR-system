import pytest
from applications.onboarding.models import Employee
from applications.leave_management.models import LeaveRequest

# Leave Request Test 
# ------------------------------
@pytest.mark.django_db
def test_create_leave_request():
    employee = Employee.objects.create(
        employee_id = 'E1000',
        employee_nin = 'cm96lkgg8908dbn',
        full_name = 'Tester test',
        email = 'testertest@gmail.com',
        job_title = 'Engineer',
        phone_number = '256772484255',
    )
    leave_request = LeaveRequest.objects.create(
        employee=employee,
        start_date='2024-12-01',
        end_date='2024-12-05',
        reason='Vacation',
    )
    assert leave_request.employee.full_name == 'Tester test'
    assert leave_request.reason == 'Vacation'
    assert leave_request.status == 'Pending'
