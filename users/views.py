from pyexpat.errors import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import Admin, Student, BaseUser
from .forms import CombinedRegistrationForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import CombinedRegistrationForm
from .utils import is_admin, is_student, get_appropriate_redirect


def logout_user(request):
    logout(request)
    return redirect('landing_page')

def register_user(request):
    if request.method == 'POST':
        form = CombinedRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Or redirect as needed
    else:
        form = CombinedRegistrationForm()

    return render(request, 'register_user.html', {'form': form})


# def login_user(request):
#     if request.method == 'POST':
#         email = request.POST['email']
#         password = request.POST['password']
#         user = authenticate(request, email=email, password=password)
#         if user is not None:
#             login(request, user)
            
#             # Check user type by querying your models
#             try:
#                 # Check if user is an Admin
#                 admin = Admin.objects.get(email=user.email)
#                 return redirect('admin_dashboard')
#             except Admin.DoesNotExist:
#                 try:
#                     # Check if user is a Student
#                     student = Student.objects.get(email=user.email) 
#                     return redirect('student_dashboard')
#                 except Student.DoesNotExist:
#                     # If neither Admin nor Student (should not happen with your setup)
#                     return redirect('landing_page')
#         else:
#             # Authentication failed
#             # Add an error message here if you want
#             pass
            
#     form = CombinedRegistrationForm()       
#     return render(request, 'login.html', {'form': form})

def landing_page(request):
    return render(request, 'landing_page.html')

# @login_required
# def admin_dashboard(request):
#     user = request.user
#     # Check if the logged-in user exists in the Admin model
#     try:
#         admin = Admin.objects.get(email=user.email)
#     except admin.DoesNotExist:
#         # Not an admin, redirect to login
#         return redirect('login')
#     users = BaseUser.objects.all()
#     return render(request, 'admin_dashboard.html', {
#         'user': users,
#     })

# @login_required
# def student_dashboard(request):
#     user = request.user
#     # Check if the logged-in user exists in the Student model
#     try:
#         student = Student.objects.get(email=user.email)
#     except student.DoesNotExist:
#         # Not a student, redirect to login
#         return redirect('login')
#     users = BaseUser.objects.all()
#     return render(request, 'student_dashboard.html', {
#         'user': users,
#     })


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
            # Optional: Add error message for failed login
            messages.error(request, 'Invalid email or password.')
            
    form = CombinedRegistrationForm()       
    return render(request, 'login.html', {'form': form})

@login_required
def admin_dashboard(request):
    user = request.user
    if not is_admin(user):
        return redirect('login')  # Redirect if the user is not an admin
    
    # Your admin dashboard logic here
    context = {
        'admin': Admin.objects.get(email=user.email),
        # Add more context data as needed
    }
    return render(request, 'admin_dashboard.html', context)

@login_required
def student_dashboard(request):
    user = request.user
    if not is_student(user):
        return redirect('login')  # Redirect if the user is not a student
    
    # Your student dashboard logic here
    context = {
        'student': Student.objects.get(email=user.email),
        # Add more context data as needed
    }
    return render(request, 'student_dashboard.html', context)