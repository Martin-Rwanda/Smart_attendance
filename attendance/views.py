from django.shortcuts import render, redirect
from .forms import ClassroomForm, CourseForm, ClassSessionForm, SeatActivityForm, AttendanceForm
from .models import Classroom, Course, ClassSession, SeatActivity, Attendance

def classroom_create(request):
    if request.method == 'POST':
        form = ClassroomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dash/classroom/classroom_list')
    else:
        form = ClassroomForm()
    return render(request, 'admin_dash/classroom/classroom_form.html', {'form': form})

def classroom_list(request):
    classrooms = Classroom.objects.all()
    return render(request, 'admin_dash/classroom/classroom_list.html', {'classrooms': classrooms})

def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dash/course/course_list')
    else:
        form = CourseForm()
    return render(request, 'admin_dash/course/course_form.html', {'form': form})

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'admin_dash/course/course_list.html', {'courses': courses})

def classsession_create(request):
    if request.method == 'POST':
        form = ClassSessionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dash/classsession/classsession_list')
    else:
        form = ClassSessionForm()
    return render(request, 'admin_dash/classsession/classsession_form.html', {'form': form})

def classsession_list(request):
    classsessions = ClassSession.objects.all()
    return render(request, 'admin_dash/classsession/classsession_list.html', {'classsessions': classsessions})

def seatactivity_create(request):
    if request.method == 'POST':
        form = SeatActivityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dash/seatactivity/seatactivity_list')
    else:
        form = SeatActivityForm()
    return render(request, 'admin_dash/seatactivity/seatactivity_form.html', {'form': form})

def seatactivity_list(request):
    seatactivities = SeatActivity.objects.all()
    return render(request, 'admin_dash/seatactivity/seatactivity_list.html', {'seatactivities': seatactivities})

# def attendance_create(request):
#     if request.method == 'POST':
#         form = AttendanceForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('attendance_list')
#     else:
#         form = AttendanceForm()
#     return render(request, 'attendance_form.html', {'form': form})

# def attendance_list(request):
#     attendances = Attendance.objects.all()
#     return render(request, 'attendance_list.html', {'attendances': attendances})