from django.contrib import admin
from .models import Course, Profile, Enrollment

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'teacher', 'price', 'created_at')
    search_fields = ('title', 'teacher__username')
    list_filter = ('teacher',)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    search_fields = ('user__username',)
    list_filter = ('role',)

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'purchased_at')
    search_fields = ('student__username', 'course__title')
    list_filter = ('purchased_at',)