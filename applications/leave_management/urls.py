from django.urls import path
from .views import LeaveRequestListView, LeaveRequestDetailView

urlpatterns = [
    path('requests/', LeaveRequestListView.as_view(), name='leave-request-list'),
    path('requests/<int:pk>/', LeaveRequestDetailView.as_view(), name='leave-request-detail'),
]