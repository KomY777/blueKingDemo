# Generated by Django 3.2.4 on 2024-12-04 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='sex',
            field=models.IntegerField(choices=[('男', '男'), ('女', '女')], verbose_name='性别'),
        ),
    ]
