from applications.onboarding.models import Employee
import pytest
from rest_framework.test import APIClient

# Employee Model Test 
# ------------------------------
@pytest.mark.django_db
def test_create_employee():
    employee = Employee.objects.create(
        employee_id = 'E1000',
        employee_nin = 'cm96lkgg8908dbn',
        full_name = 'Tester test',
        email = 'testertest@gmail.com',
        job_title = 'Engineer',
        phone_number = '256772484255',
    )
    assert employee.full_name == 'Tester test'
    assert employee.email == 'testertest@gmail.com'


# Employee API POST GET URL Test 
# -------------------------------------
@pytest.mark.django_db
def test_employee_api():
    client = APIClient()

    # Create an employee
    response = client.post("/api/onboarding/employees/", {
        "employee_id" : "E1000",
        "employee_nin" : "cm96lkgg8908dbn",
        "full_name" : "Tester test",
        "email" : "testertest@gmail.com",
        "job_title" : "Engineer",
        "phone_number" : "256772484255",
    })
    assert response.status_code == 201

    # Get the employee
    response = client.get("/api/onboarding/employees/")
    assert response.status_code == 200
    assert len(response.data) == 1