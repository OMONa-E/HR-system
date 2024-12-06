# HR System Application

#### Human Resource Management System Web Application API

## 2. Introduction

### Problem Statement:
Managing HR processes like employee onboarding, attendance, leave management, and reporting is often inefficient and prone to errors in many organizations.

### Goals:
- Build a centralized system to streamline HR processes.
- Provide secure, scalable, and user-friendly solutions.

## 3. Background and History

### Why This Project?
- Inefficient manual HR processes result in delays and errors.
- The need for a lightweight, backend-focused solution to integrate with any frontend.

### Challenges/Gaps:
- Difficulty managing user authentication for multiple devices.
- Ensuring role-based access without interruptions.

## 4. Project Overview

### Core Features:
- User Management: CRUD-L for users with roles like Admin, Manager, and Employee.
- Authentication: Secure login, logout, and multi-device support.
- Employee Onboarding: Adding and managing employee profiles.
- Attendance Tracking: Clock-in/out and attendance reports.
- Leave Management: Request and approve/reject leaves.
- Reporting: Generate insights and export data.

### Tech Stack:
- Backend: Django, Django REST Framework.
- Database: PostgreSQL.
- Authentication: JWT with djangorestframework-simplejwt.

## 5. Implementation

### Development Steps:
1. Setup github repo and clone
2. Setup local python environment 
3. Setup Django + the neccessary stack and database - postgreSQL.
4. Implement CRUD-L for Users and Profiles.
5. Add role-based access control (RBAC).
6. Build multi-device login and logout functionality.
7. Develop core HR features: Onboarding, Attendance, Leave Management.
8. Integrate reporting with Matplotlib for visualizations and export as CSV.
9. Setup .github/workflows as .yml file for CI/CD
10. Setup pytest for all api endpoints
11. Deploy

### Key API Endpoints:
- POST /api/onboarding/users/: Create a new user.
- POST /api/token/: Login and obtain tokens.
- POST /logout/: Logout from a device.
- GET /active-devices/: List active device sessions.

## 6. Challenges and Solutions

### Challenges:
- Token management for multi-device support.
- Integrating secure authentication and role-based access.
- Handling user-friendly error responses.
- Documentation with drf-spectacular for function base views

### Solutions:
- Implemented UserDevice model for session tracking.
- Used djangorestframework-simplejwt for JWT handling.
- Added robust testing with pytest to ensure reliability.
- Document every class method

## 8. Future Improvements

### Potential Features and Todo:
- Integrate with a frontend framework like React or Vue.js.
- Add payroll management.
- Build detailed analytics.
- Use of Docker and Kubernator
- Use of Microservices Sytem Design Principle
