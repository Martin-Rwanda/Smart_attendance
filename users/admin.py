
from django.contrib import admin
from .models import Admin, Student, LectureUser

# Register your models here.
admin.site.register(Admin)
admin.site.register(Student)
admin.site.register(LectureUser)  