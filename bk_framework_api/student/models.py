from django.db import models

# Create your models here.
class Student(models.Model):

    class Gender(models.TextChoices):
        MALE='男'
        FEMALE='女'
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100,verbose_name="姓名")
    student_code=models.IntegerField(null=False,verbose_name="学号")
    sex=models.CharField(max_length=1,choices=((Gender.MALE,'男'),(Gender.FEMALE,'女')),verbose_name="性别")
    update_time = models.DateTimeField(auto_now=True,verbose_name="更新时间")

    class Meta:
        db_table='student'
        verbose_name='学生表'