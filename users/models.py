from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create a custom user manager to handle user creation
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

# Base user model for both Admin and Student
class BaseUser(AbstractBaseUser):
    first_name = models.CharField(max_length=100)
    second_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=15)
    password = models.CharField(max_length=255)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'second_name', 'telephone']

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.first_name} {self.second_name}'

# Admin model extending BaseUser
class Admin(BaseUser):
    is_admin = models.BooleanField(default=True)
    is_head_of_faculty = models.BooleanField(default=False)  # Whether the admin is head of faculty

    def __str__(self):
        return f'Admin: {self.first_name} {self.second_name}'

# Student model extending BaseUser
class Student(BaseUser):
    session = models.CharField(max_length=10, choices=[
        ('DAY', 'Day'),
        ('EVENING', 'Evening'),
        ('WEEKEND', 'Weekend'),
    ], default='DAY')
    student_id = models.CharField(max_length=15, unique=True)
    fingerprint = models.CharField(max_length=255, null=True, blank=True)  # Assuming fingerprint is a string identifier

    def __str__(self):
        return f'Student: {self.first_name} {self.second_name}, Session: {self.session}, ID: {self.student_id}'
