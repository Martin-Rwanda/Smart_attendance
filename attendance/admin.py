from django.contrib import admin
from .models import Course

class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'lectureuser')  # Add 'lectureuser' to the list display
    list_filter = ('lectureuser',)  # Add 'lectureuser' to the filters
    search_fields = ('name', 'code', 'lectureuser__email')  # Add 'lectureuser' to the search fields

admin.site.register(Course, CourseAdmin)