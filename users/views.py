from pyexpat.errors import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import Admin, Student, BaseUser
from .forms import CombinedRegistrationForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import CombinedRegistrationForm
from .utils import is_admin, is_student, get_appropriate_redirect
from django.core.paginator import Paginator
from django.contrib import messages 


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
    
    
    # context = {
    #     'admin': Admin.objects.get(email=user.email),
    #     # Add more context data as needed
        
    # }
    return render(request, 'admin_dash/admin_dashboard.html', {'page_obj': page_obj})

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
    return render(request, 'student_dash/student_dashboard.html', context)

@login_required
def student_records(request):
    students = Student.objects.all()
    paginator = Paginator(students, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'admin_dash/studentrec.html', {'page_obj': page_obj})