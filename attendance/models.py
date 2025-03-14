from django.db import models
from django.utils import timezone
from datetime import timedelta

from users.models import Student
from users.models import Student, LectureUser  

class Classroom(models.Model):
    """Model to represent a physical classroom"""
    name = models.CharField(max_length=100)
    building = models.CharField(max_length=100)
    floor = models.CharField(max_length=10)
    room_number = models.CharField(max_length=10)
    capacity = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.building} - {self.room_number}: {self.name}"

class Course(models.Model):
    """Model to represent a course that has scheduled sessions in classrooms"""
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True, null=True)
    
    # Session types this course is offered in
    SESSION_CHOICES = [
        ('DAY', 'Day'),
        ('EVENING', 'Evening'),
        ('WEEKEND', 'Weekend'),
    ]
    sessions_offered = models.CharField(max_length=100)  # Store as comma-separated values
    lectureuser = models.ForeignKey(LectureUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='courses')  # Add this field
    
    def get_sessions_list(self):
        """Return the sessions offered as a list"""
        return self.sessions_offered.split(',')
    
    def set_sessions_list(self, sessions_list):
        """Set sessions offered from a list"""
        self.sessions_offered = ','.join(sessions_list)
    
    def __str__(self):
        return f"{self.code}: {self.name}"

class ClassSession(models.Model):
    """Model to represent a scheduled class session"""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="class_sessions")
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    # Session type
    SESSION_CHOICES = [
        ('DAY', 'Day'),
        ('EVENING', 'Evening'),
        ('WEEKEND', 'Weekend'),
    ]
    session_type = models.CharField(max_length=10, choices=SESSION_CHOICES, default='DAY')
    
    def __str__(self):
        return f"{self.course} - {self.get_session_type_display()} - {self.date} ({self.start_time} to {self.end_time})"
    
    def get_enrolled_students(self):
        """Get all students enrolled in this session type"""
        return Student.objects.filter(session=self.session_type)
    
    class Meta:
        ordering = ['date', 'start_time']

class SeatActivity(models.Model):
    """
    Model to track when a student leaves their seat during class
    Connected to chair sensors
    """
    student = models.ForeignKey('users.Student', on_delete=models.CASCADE)
    class_session = models.ForeignKey(ClassSession, on_delete=models.CASCADE)
    
    # When student left their seat
    left_seat_time = models.DateTimeField()
    
    # When student returned to seat (null if they haven't returned yet)
    returned_seat_time = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        duration = "In progress" if not self.returned_seat_time else f"{self.absence_duration} minutes"
        return f"{self.student} - Left seat at {self.left_seat_time.time()} - Duration: {duration}"
    
    @property
    def absence_duration(self):
        """Calculate how long the student was away from their seat in minutes"""
        if not self.returned_seat_time:
            # If student hasn't returned, calculate against current time
            return (timezone.now() - self.left_seat_time).total_seconds() / 60
        return (self.returned_seat_time - self.left_seat_time).total_seconds() / 60
    
    @property
    def is_extended_absence(self):
        """Check if absence is longer than 10 minutes"""
        return self.absence_duration > 10

class Attendance(models.Model):
    """
    Model to track student attendance using fingerprint and seat sensors
    """
    student = models.ForeignKey('users.Student', on_delete=models.CASCADE, related_name="attendances")
    class_session = models.ForeignKey(ClassSession, on_delete=models.CASCADE, related_name="attendances")
    
    # Track when the student entered the classroom
    entry_time = models.DateTimeField(null=True, blank=True)
    entry_fingerprint_verified = models.BooleanField(default=False)
    
    # Track when the student left the classroom
    exit_time = models.DateTimeField(null=True, blank=True)
    exit_fingerprint_verified = models.BooleanField(default=False)
    
    # Automatic timestamps for record-keeping
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Flag for extended absence (over 10 minutes)
    had_extended_absence = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['student', 'class_session']
        ordering = ['-class_session__date', '-class_session__start_time']
    
    def __str__(self):
        status = self.attendance_status
        return f"{self.student} - {self.class_session} - {status}"
    
    @property
    def attendance_status(self):
        """Determine attendance status based on entry/exit and seat activity"""
        # If student had an extended absence, mark as absent
        if self.had_extended_absence:
            return "Absent (Extended Leave)"
            
        if not self.entry_time:
            return "Absent"
        elif not self.exit_time:
            return "Present (No Exit Recorded)"
        
        # Calculate duration in class
        duration = (self.exit_time - self.entry_time).total_seconds() / 60  # in minutes
        class_duration = (self.class_session.end_time.hour * 60 + self.class_session.end_time.minute) - \
                         (self.class_session.start_time.hour * 60 + self.class_session.start_time.minute)
        
        # If student attended at least 75% of the class
        if duration >= (class_duration * 0.75):
            return "Present"
        elif duration >= (class_duration * 0.5):
            return "Late/Left Early"
        else:
            return "Insufficient Attendance"
    
    def record_entry(self, fingerprint_verified=True):
        """Record student entry to classroom"""
        self.entry_time = timezone.now()
        self.entry_fingerprint_verified = fingerprint_verified
        self.save()
    
    def record_exit(self, fingerprint_verified=True):
        """Record student exit from classroom"""
        self.exit_time = timezone.now()
        self.exit_fingerprint_verified = fingerprint_verified
        self.save()
    
    def check_seat_activities(self):
        """
        Check if student had any extended absences during class
        and update attendance status accordingly
        """
        seat_activities = SeatActivity.objects.filter(
            student=self.student,
            class_session=self.class_session
        )
        
        # Check for any extended absences (> 10 minutes)
        for activity in seat_activities:
            if activity.is_extended_absence:
                self.had_extended_absence = True
                self.save()
                return True
                
        return False

# Helper function for session verification
def verify_student_session_match(student, class_session):
    """
    Verify that a student is in the right session for a class
    Returns True if sessions match, False otherwise
    """
    return student.session == class_session.session_type

# Function to handle fingerprint scan for attendance
def process_fingerprint_scan(fingerprint_data, classroom_id):
    """
    Process fingerprint scan for attendance
    
    Parameters:
    - fingerprint_data: The fingerprint data from scanner
    - classroom_id: ID of the classroom where scan occurred
    
    Returns:
    - (student, message) tuple: student object and status message
    """
    try:
        # Find student by fingerprint
        student = Student.objects.get(fingerprint=fingerprint_data)
        
        # Get current time
        now = timezone.now()
        
        # Find active class session in this classroom
        class_session = ClassSession.objects.filter(
            classroom_id=classroom_id,
            date=now.date(),
            start_time__lte=now.time(),
            end_time__gte=now.time(),
            session_type=student.session  # Match student's session type
        ).first()
        
        if not class_session:
            return student, "No active class session found for your session type"
        
        # Check if we already have an attendance record
        attendance, created = Attendance.objects.get_or_create(
            student=student,
            class_session=class_session
        )
        
        # If student hasn't checked in yet, this is an entry
        if not attendance.entry_time:
            attendance.record_entry()
            return student, "Entry recorded successfully"
        
        # If student has checked in but not out, this is an exit
        elif not attendance.exit_time:
            attendance.record_exit()
            return student, "Exit recorded successfully"
        
        # Student has already checked in and out
        else:
            return student, "You have already checked in and out for this class"
            
    except Student.DoesNotExist:
        return None, "Fingerprint not recognized"
    except Exception as e:
        return None, f"Error: {str(e)}"
    


class ModuleRegistration(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='module_registrations')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='module_registrations')
    is_rejected = models.BooleanField(default=False)  # To track if the student rejected the module

    class Meta:
        unique_together = ['student', 'course']  

    def __str__(self):
        return f"{self.student} - {self.course}"