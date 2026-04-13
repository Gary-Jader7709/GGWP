from django.db import models

class Course(models.Model):
    title = models.CharField(max_length=200, verbose_name="課程名稱")
    teacher = models.CharField(max_length=100, verbose_name="講師")
    price = models.IntegerField(verbose_name="價格")
    description = models.TextField(verbose_name="課程介紹")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="建立時間")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "課程"
        verbose_name_plural = "課程管理"