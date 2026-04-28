from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('register/', views.register, name='register'),
    path('register-success/', views.register_success, name='register_success'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),

    path('course/<int:course_id>/buy/', views.buy_course, name='buy_course'),
    path('course/<int:course_id>/purchase-success/', views.purchase_success, name='purchase_success'),

    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='main/password_reset.html'
    ), name='password_reset'),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='main/password_reset_done.html'
    ), name='password_reset_done'),
    path('my-courses/', views.my_courses, name='my_courses'),
    path('profile/', views.profile_view, name='profile'),
]