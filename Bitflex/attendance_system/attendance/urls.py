from django.urls import path
from . import views

urlpatterns = [
    path('punch/', views.punch_attendace, name='punch-attendance'),
    path('view/', views.view_attendance, name='view-attendance'),
]