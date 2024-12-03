from django.urls import path
from .views import AttendanceLogDetailView, AttendanceLogListView

urlpatterns = [
    path('logs/', AttendanceLogListView.as_view(), name='attendance-log'),
    path('logs/<int:pk>/', AttendanceLogDetailView.as_view(), name='attendance-detail'),
]
