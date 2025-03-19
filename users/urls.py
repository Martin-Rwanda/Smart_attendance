from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('register/', views.register_user, name='register_user'),
    path('login/', views.login_user, name='login'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('lectureuser_dashboard/', views.lectureuser_dashboard, name='lectureuser_dashboard'),
    path('logout/', views.logout_user, name='logout'),
    path('student-records/', views.student_records, name='student_records'),
    path('lecture-records/', views.lecture_records, name='lecture_records'),
    path('lecturer/dashboard/', views.lectureuser_dashboard, name='lectureuser_dashboard'),
    path('lecturer/course/<int:course_id>/students/', views.registered_students, name='registered_students'),
    path('lecturer/all-students/', views.all_registered_students, name='all_registered_students'),
    path('get_fingerprint/', views.get_fingerprint, name='get_fingerprint'),
    path('send_to_arduino/', views.send_to_arduino, name='send_to_arduino'),
]