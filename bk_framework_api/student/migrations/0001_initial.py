# Generated by Django 3.2.4 on 2024-12-02 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, verbose_name='姓名')),
                ('student_code', models.IntegerField(verbose_name='学号')),
                ('sex', models.CharField(max_length=1, verbose_name='性别')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '学生表',
                'db_table': 'student',
            },
        ),
    ]
