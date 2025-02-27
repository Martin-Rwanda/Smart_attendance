from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('register/', views.register_user, name='register_user'),
    path('login/', views.login_user, name='login'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('logout/', views.logout_user, name='logout'),
    path('student-records/', views.student_records, name='student_records'),
]

