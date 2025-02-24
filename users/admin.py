from django.contrib import admin

# Register your models here.
from .models import Admin, Student

admin.site.register(Admin)
admin.site.register(Student)
