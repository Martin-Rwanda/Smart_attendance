from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import Admin, Student
from .forms import CombinedRegistrationForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

def logout_user(request):
    logout(request)
    return redirect('landing_page')

def landing_page(request):
    return render(request, 'landing_page.html')

@login_required
def admin_dashboard(request):
    if not isinstance(request.user, Admin):
        return redirect('login')  # Redirect if the user is not an admin
    return render(request, 'admin_dashboard.html')

@login_required
def student_dashboard(request):
    if not isinstance(request.user, Student):
        return redirect('login')  # Redirect if the user is not a student
    return render(request, 'student_dashboard.html')

def register_user(request):
    if request.method == 'POST':
        form = CombinedRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Or redirect as needed
    else:
        form = CombinedRegistrationForm()

    return render(request, 'register_user.html', {'form': form})


def login_user(request):
    if request.user.is_authenticated:
        # Redirect to a page depending on user type
        if isinstance(request.user, Admin):
            return redirect('admin_dashboard')
        elif isinstance(request.user, Student):
            return redirect('student_dashboard')
        
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            if isinstance(user, Admin):  # Check if the user is an Admin
                return redirect('admin_dashboard')
            elif isinstance(user, Student):  # Check if the user is a Student
                return redirect('student_dashboard')  # Redirect student to their specific dashboard 
            else:
                return redirect('landing_page')  # Redirect to landing page after login
            
    return render(request, 'login.html')