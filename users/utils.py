# Add these functions to a utils.py file in your app
def is_admin(user):
    """Helper function to check if a user is an admin"""
    from .models import Admin  # Import locally to avoid circular imports
    return Admin.objects.filter(email=user.email).exists()

def is_student(user):
    """Helper function to check if a user is a student"""
    from .models import Student  # Import locally to avoid circular imports
    return Student.objects.filter(email=user.email).exists()

def get_user_type(user):
    """Helper function to get user type as string"""
    if is_admin(user):
        return "admin"
    elif is_student(user):
        return "student"
    else:
        return "unknown"

def get_appropriate_redirect(user):
    """Helper function to determine the appropriate redirect for a user"""
    if is_admin(user):
        return 'admin_dashboard'
    elif is_student(user):
        return 'student_dashboard'
    else:
        return 'landing_page'