from django.shortcuts import render, redirect , get_object_or_404
from .forms import ClassroomForm, CourseForm, ClassSessionForm, SeatActivityForm, AttendanceForm
from .models import Classroom, Course, ClassSession, SeatActivity, Attendance 
from django.contrib import messages
from .models import ModuleRegistration
from users.models import Student
from django.contrib.auth.decorators import login_required 

def classroom_create(request):
    if request.method == 'POST':
        form = ClassroomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('classroom_list')
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
            return redirect('course_list')
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
            return redirect('classsession_list')
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


def module_register(request):
    # Fetch the logged-in student
    student = request.user.student 

    # Fetch all courses that match the student's session
    available_courses = Course.objects.filter(sessions_offered__contains=student.session)

    # Handle registration/rejection request
    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        action = request.POST.get('action') 

        if course_id and action:
            course = Course.objects.get(id=course_id)

            if action == 'register':
                ModuleRegistration.objects.create(student=student, course=course)
                messages.success(request, f'Successfully registered for {course.name}!')
            elif action == 'reject':
                ModuleRegistration.objects.create(student=student, course=course, is_rejected=True)
                messages.success(request, f'Successfully rejected {course.name}.')

    # Fetch the student's registered and rejected modules
    registered_modules = ModuleRegistration.objects.filter(student=student, is_rejected=False).select_related('course')
    rejected_modules = ModuleRegistration.objects.filter(student=student, is_rejected=True)

    # Exclude registered and rejected modules from the available courses
    available_courses = available_courses.exclude(
        id__in=registered_modules.values_list('course_id', flat=True)
    ).exclude(
        id__in=rejected_modules.values_list('course_id', flat=True)
    )

    return render(request, 'student_dash/modules/register.html', {
        'available_courses': available_courses,
        'registered_modules': registered_modules,
    })


def modules(request):
    # Fetch the logged-in student
    student = request.user.student 

    # Fetch all courses that match the student's session
    available_courses = Course.objects.filter(sessions_offered__contains=student.session)        

    # Fetch the student's registered and rejected modules
    registered_modules = ModuleRegistration.objects.filter(student=student, is_rejected=False).select_related('course')

    return render(request, 'student_dash/modules/modules.html', {
        'available_courses': available_courses,
        'registered_modules': registered_modules,
    })



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