from django.urls import path
from . import views

urlpatterns = [
    path('classroom/create/', views.classroom_create, name='classroom_create'),
    path('classroom/list/', views.classroom_list, name='classroom_list'),
    path('course/create/', views.course_create, name='course_create'),
    path('course/list/', views.course_list, name='course_list'),
    path('classsession/create/', views.classsession_create, name='classsession_create'),
    path('', views.classsession_list, name='classsession_list'),
    path('seatactivity/create/', views.seatactivity_create, name='seatactivity_create'),
    path('seatactivity/list/', views.seatactivity_list, name='seatactivity_list'),
    # path('attendance/create/', views.attendance_create, name='attendance_create'),
    # path('attendance/list/', views.attendance_list, name='attendance_list'),
]