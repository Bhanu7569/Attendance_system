from django.shortcuts import render
from django.utils.timezone import localtime, now
from .models import Employee, Attendance
from datetime import datetime

def punch_attendace(request):
    message = ''

    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')

        try:
            employee = Employee.objects.get(employee_id=employee_id)
            today = localtime().date()

            attendance, created = Attendance.objects.get_or_create(employee=employee, date=today)

            current_time = localtime().time()  # Get current local time

            if not attendance.in_time:
                attendance.in_time = current_time
                attendance.save()
                message = "In-Time recorded successfully."
            elif not attendance.out_time:
                attendance.out_time = current_time
                attendance.save()
                message = "Out-Time recorded successfully."
            else:
                message = "You have already marked Both In-time and Out-time today. Please try again tomorrow."

        except Employee.DoesNotExist:
            message = "Invalid Employee ID. Please Try again."

    return render(request, 'attendance/punch.html', {'message': message})


def view_attendance(request):
    attendance_records = Attendance.objects.select_related('employee').order_by('-date', '-in_time')

    # Calculate worked hours
    attendance_data = []
    for record in attendance_records:
        worked_hours = "-"
        if record.in_time and record.out_time:
            in_datetime = datetime.combine(record.date, record.in_time)
            out_datetime = datetime.combine(record.date, record.out_time)
            duration = out_datetime - in_datetime
            total_seconds = duration.total_seconds()
            hours = int(total_seconds // 3600)
            minutes = int((total_seconds % 3600) // 60)
            worked_hours = f"{hours}h {minutes}m"

        attendance_data.append({
            'employee': record.employee,
            'date': record.date,
            'in_time': record.in_time,
            'out_time': record.out_time,
            'worked_hours': worked_hours
        })

    return render(request, 'attendance/view_attendance.html', {'attendance_records': attendance_data})
