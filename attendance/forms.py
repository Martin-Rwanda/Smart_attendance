from django import forms
from .models import Classroom, Course, ClassSession, SeatActivity, Attendance
from users.models import Student, LectureUser 
from django.utils import timezone

class ClassroomForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = ['name', 'building', 'floor', 'room_number', 'capacity']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'building': forms.TextInput(attrs={'class': 'form-control'}),
            'floor': forms.TextInput(attrs={'class': 'form-control'}),
            'room_number': forms.TextInput(attrs={'class': 'form-control'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class CourseForm(forms.ModelForm):
    # Define session choices for sessions_offered
    SESSION_CHOICES = [
        ('DAY', 'Day'),
        ('EVENING', 'Evening'),
        ('WEEKEND', 'Weekend'),
    ]

    # Update sessions_offered to use ChoiceField
    sessions_offered = forms.ChoiceField(
        choices=SESSION_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True,
    )

    class Meta:
        model = Course
        fields = ['name', 'code', 'description', 'sessions_offered', 'lectureuser']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'lectureuser': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['lectureuser'].label_from_instance = lambda obj: f"{obj.first_name} {obj.second_name}"

class ClassSessionForm(forms.ModelForm):
    class Meta:
        model = ClassSession
        fields = ['course', 'classroom', 'date', 'start_time', 'end_time', 'session_type']
        widgets = {
            'course': forms.Select(attrs={'class': 'form-control'}),
            'classroom': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'session_type': forms.Select(attrs={'class': 'form-control'}),
        }

class SeatActivityForm(forms.ModelForm):
    class Meta:
        model = SeatActivity
        fields = ['student', 'class_session', 'left_seat_time', 'returned_seat_time']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'class_session': forms.Select(attrs={'class': 'form-control'}),
            'left_seat_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'returned_seat_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'class_session', 'entry_time', 'entry_fingerprint_verified', 'exit_time', 'exit_fingerprint_verified', 'had_extended_absence']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'class_session': forms.Select(attrs={'class': 'form-control'}),
            'entry_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'exit_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'entry_fingerprint_verified': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'exit_fingerprint_verified': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'had_extended_absence': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }