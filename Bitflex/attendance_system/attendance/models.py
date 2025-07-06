from django.db import models
from django.utils import timezone

class Employee(models.Model):
    employee_id = models.CharField(max_length=4, unique=True)
    name = models.CharField(max_length=100, default='unknown')

    def __str__(self):
        return self.employee_id

class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    in_time = models.TimeField(null=True, blank=True)
    out_time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.employee.employee_id} - {self.date}"
