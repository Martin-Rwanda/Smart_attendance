from django import forms
from .models import Admin, Student, LectureUser

class CombinedRegistrationForm(forms.Form):
    # Common fields for all user types
    first_name = forms.CharField(max_length=100)
    second_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    telephone = forms.CharField(max_length=15)
    password = forms.CharField(widget=forms.PasswordInput)
    
    # Conditional fields based on user type
    user_type = forms.ChoiceField(choices=[
        ('admin', 'Admin'), 
        ('student', 'Student'), 
        ('lectureuser', 'Lecture'),
    ])
    
    # Student-specific fields
    session = forms.CharField(max_length=15, required=False)
    student_id = forms.CharField(max_length=15, required=False)  # Only for students
    fingerprint = forms.CharField(max_length=255, required=False)  # Only for students
    
    # Admin-specific fields
    is_head_of_faculty = forms.BooleanField(required=False)  # Only for admins
    
    # LectureUser-specific fields
    department = forms.CharField(max_length=100, required=False)  # Only for lecture users
    
    def save(self):
        user_type = self.cleaned_data['user_type']
        
        if user_type == 'admin':
            # Admin Registration
            admin = Admin(
                first_name=self.cleaned_data['first_name'],
                second_name=self.cleaned_data['second_name'],
                email=self.cleaned_data['email'],
                telephone=self.cleaned_data['telephone'],
                is_head_of_faculty=self.cleaned_data['is_head_of_faculty']
            )
            admin.set_password(self.cleaned_data['password'])
            admin.save()
            return admin
        
        elif user_type == 'student':
            # Student Registration
            student = Student(
                first_name=self.cleaned_data['first_name'],
                second_name=self.cleaned_data['second_name'],
                email=self.cleaned_data['email'],
                telephone=self.cleaned_data['telephone'],
                student_id=self.cleaned_data['student_id'],
                session=self.cleaned_data['session'],
                fingerprint=self.cleaned_data['fingerprint']
            )
            student.set_password(self.cleaned_data['password'])
            student.save()
            return student
        
        elif user_type == 'lectureuser':
            # LectureUser Registration
            lectureuser = LectureUser(
                first_name=self.cleaned_data['first_name'],
                second_name=self.cleaned_data['second_name'],
                email=self.cleaned_data['email'],
                telephone=self.cleaned_data['telephone'],
                department=self.cleaned_data['department'],
            )
            lectureuser.set_password(self.cleaned_data['password'])
            lectureuser.save()
            return lectureuser