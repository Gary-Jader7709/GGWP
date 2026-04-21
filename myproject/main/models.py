from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ROLE_CHOICES = [
        ('student', '學生'),
        ('teacher', '老師'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="使用者")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, verbose_name="角色")

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"

    class Meta:
        verbose_name = "使用者資料"
        verbose_name_plural = "使用者資料"

class Course(models.Model):
    title = models.CharField(max_length=200, verbose_name="課程名稱")
    teacher = models.CharField(max_length=100, verbose_name="講師")
    price = models.IntegerField(verbose_name="價格")
    description = models.TextField(verbose_name="課程介紹")
    image = models.ImageField(upload_to='course_images/', verbose_name="課程圖片", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="建立時間")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "課程"
        verbose_name_plural = "課程管理"

class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="學生")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="課程")
    purchased_at = models.DateTimeField(auto_now_add=True, verbose_name="購買時間")

    def __str__(self):
        return f"{self.student.username} - {self.course.title}"

    class Meta:
        verbose_name = "購課紀錄"
        verbose_name_plural = "購課紀錄"
        unique_together = ('student', 'course')