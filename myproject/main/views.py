from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Course, Profile, Enrollment
from .forms import RegisterForm

def home(request):
    courses = Course.objects.all()
    return render(request, 'main/home.html', {'courses': courses})

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    already_purchased = False
    if request.user.is_authenticated:
        already_purchased = Enrollment.objects.filter(student=request.user, course=course).exists()

    return render(request, 'main/course_detail.html', {
        'course': course,
        'already_purchased': already_purchased
    })

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )

            Profile.objects.create(
                user=user,
                role=form.cleaned_data['role']
            )

            return redirect('register_success')
    else:
        form = RegisterForm()

    return render(request, 'main/register.html', {'form': form})

def register_success(request):
    return render(request, 'main/register_success.html')

def login_view(request):
    error_message = None

    if request.method == 'POST':
        login_input = request.POST.get('username')
        password = request.POST.get('password')

        if '@' in login_input:
            try:
                user_obj = User.objects.get(email=login_input)
                username = user_obj.username
            except User.DoesNotExist:
                username = login_input
        else:
            username = login_input

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if user.is_superuser:
                return redirect('/admin/')

            try:
                profile = user.profile
                if profile.role == 'teacher':
                    return redirect('teacher_dashboard')
                elif profile.role == 'student':
                    return redirect('student_dashboard')
                else:
                    return redirect('home')
            except Profile.DoesNotExist:
                return redirect('home')
        else:
            error_message = '帳號 / Email 或密碼錯誤。'

    return render(request, 'main/login.html', {'error_message': error_message})

@login_required
def my_courses(request):
    try:
        profile = request.user.profile
        if profile.role != 'student':
            return redirect('home')
    except Profile.DoesNotExist:
        return redirect('home')

    enrollments = Enrollment.objects.filter(student=request.user).select_related('course')
    return render(request, 'main/my_courses.html', {'enrollments': enrollments})
def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def student_dashboard(request):
    try:
        profile = request.user.profile
        if profile.role != 'student':
            return redirect('home')
    except Profile.DoesNotExist:
        return redirect('home')

    return render(request, 'main/student_dashboard.html')

@login_required
def teacher_dashboard(request):
    try:
        profile = request.user.profile
        if profile.role != 'teacher':
            return redirect('home')
    except Profile.DoesNotExist:
        return redirect('home')

    teacher_courses = Course.objects.filter(teacher=request.user)

    course_data = []
    for course in teacher_courses:
        purchase_count = Enrollment.objects.filter(course=course).count()
        course_data.append({
            'course': course,
            'purchase_count': purchase_count,
        })

    return render(request, 'main/teacher_dashboard.html', {
        'course_data': course_data
    })

@login_required
def buy_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        return redirect('home')

    enrollment, created = Enrollment.objects.get_or_create(
        student=request.user,
        course=course
    )

    return redirect('purchase_success', course_id=course.id)

    enrollment, created = Enrollment.objects.get_or_create(
        student=request.user,
        course=course
    )

    return redirect('purchase_success', course_id=course.id)

@login_required
def purchase_success(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'main/purchase_success.html', {'course': course})
@login_required
def profile_view(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        return redirect('home')

    return render(request, 'main/profile.html', {
        'profile': profile
    })