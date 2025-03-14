from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login
from .models import Admin, Student, LectureUser, BaseUser
from .forms import CombinedRegistrationForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from users.models import LectureUser  
from attendance.models import Course, ModuleRegistration

def logout_user(request):
    logout(request)
    return redirect('landing_page')


def register_user(request):
    if request.method == 'POST':
        form = CombinedRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CombinedRegistrationForm()

    return render(request, 'register_user.html', {'form': form})


def landing_page(request):
    return render(request, 'landing_page.html')


def login_user(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            # Redirect based on user type
            return redirect(get_appropriate_redirect(user))
        else:
            messages.error(request, 'Invalid email or password.')

    form = CombinedRegistrationForm()
    return render(request, 'login.html', {'form': form})


@login_required
def admin_dashboard(request):
    user = request.user
    students = Student.objects.all()
    paginator = Paginator(students, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if not is_admin(user):
        return redirect('login')  # Redirect if the user is not an admin

    return render(request, 'admin_dash/admin_dashboard.html', {'page_obj': page_obj})


@login_required
def student_dashboard(request):
    user = request.user
    if not is_student(user):
        return redirect('login')  # Redirect if the user is not a student

    context = {
        'student': Student.objects.get(email=user.email),
        # Add more context data as needed
    }
    return render(request, 'student_dash/student_dashboard.html', context)



@login_required
def lectureuser_dashboard(request):
    user = request.user
    if not is_lectureuser(user):
        return redirect('login')  # Redirect if the user is not a lecture user

    # Fetch the logged-in lecturer
    lecturer = LectureUser.objects.get(email=user.email)

    # Fetch courses assigned to the lecturer
    courses = Course.objects.filter(lectureuser=lecturer)

    context = {
        'lectureuser': lecturer,
        'courses': courses,  # Pass courses to the template
    }
    return render(request, 'lecture_dash/lecture_dashboard.html', context)

@login_required
def registered_students(request, course_id):
    # Fetch the logged-in lecturer
    lecturer = request.user.lectureuser  

    # Fetch the course
    course = get_object_or_404(Course, id=course_id)

    # Check if the logged-in lecturer is assigned to the course
    if course.lectureuser != lecturer:
        messages.error(request, "You are not authorized to view this course.")
        return redirect('lectureuser_dashboard')

    # Fetch students registered for the course
    registered_students = ModuleRegistration.objects.filter(
        course=course, is_rejected=False
    ).select_related('student')

    return render(request, 'lecture_dash/registered_students.html', {
        'course': course,
        'registered_students': registered_students,
    })


@login_required
def all_registered_students(request):
    # Fetch the logged-in lecturer
    lecturer = request.user.lectureuser  # Assuming the logged-in user is a lecturer

    # Fetch all courses taught by the lecturer
    courses = Course.objects.filter(lectureuser=lecturer)

    # Create a dictionary to store registered students for each course
    course_students = {}

    for course in courses:
        # Fetch students registered for the course
        registered_students = ModuleRegistration.objects.filter(
            course=course, is_rejected=False
        ).select_related('student')

        # Debug: Print the course and the number of registered students
        print(f"Course: {course.name}, Students: {registered_students.count()}")

        course_students[course] = registered_students

    return render(request, 'lecture_dash/allstudents.html', {
        'course_students': course_students,
    })

@login_required
def student_records(request):
    students = Student.objects.all()
    paginator = Paginator(students, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'admin_dash/studentrec.html', {'page_obj': page_obj})

@login_required
def lecture_records(request):
    # Fetch all LectureUser records
    lecture_users = LectureUser.objects.all()

    # Paginate the records (10 records per page)
    paginator = Paginator(lecture_users, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin_dash/lecturerec.html', {'page_obj': page_obj})

# Utility Functions (if they exist in your code)
def is_admin(user):
    return hasattr(user, 'admin')


def is_student(user):
    return hasattr(user, 'student')


def is_lectureuser(user):
    return hasattr(user, 'lectureuser')


def get_appropriate_redirect(user):
    if is_admin(user):
        return 'admin_dashboard'
    elif is_student(user):
        return 'student_dashboard'
    elif is_lectureuser(user):
        return 'lectureuser_dashboard'
    else:
        return 'landing_page'