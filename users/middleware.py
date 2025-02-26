from .utils import get_user_type, is_admin, is_student

class UserTypeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Add user type info to request if user is authenticated
        if request.user.is_authenticated:
            request.user_type = get_user_type(request.user)
            request.is_admin_user = is_admin(request.user)
            request.is_student_user = is_student(request.user)
        
        response = self.get_response(request)
        return response