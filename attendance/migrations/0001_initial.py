# Generated by Django 5.1.6 on 2025-03-02 10:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Classroom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('building', models.CharField(max_length=100)),
                ('floor', models.CharField(max_length=10)),
                ('room_number', models.CharField(max_length=10)),
                ('capacity', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=20, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('sessions_offered', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ClassSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('session_type', models.CharField(choices=[('DAY', 'Day'), ('EVENING', 'Evening'), ('WEEKEND', 'Weekend')], default='DAY', max_length=10)),
                ('classroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance.classroom')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='class_sessions', to='attendance.course')),
            ],
            options={
                'ordering': ['date', 'start_time'],
            },
        ),
        migrations.CreateModel(
            name='SeatActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('left_seat_time', models.DateTimeField()),
                ('returned_seat_time', models.DateTimeField(blank=True, null=True)),
                ('class_session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance.classsession')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.student')),
            ],
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entry_time', models.DateTimeField(blank=True, null=True)),
                ('entry_fingerprint_verified', models.BooleanField(default=False)),
                ('exit_time', models.DateTimeField(blank=True, null=True)),
                ('exit_fingerprint_verified', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('had_extended_absence', models.BooleanField(default=False)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendances', to='users.student')),
                ('class_session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendances', to='attendance.classsession')),
            ],
            options={
                'ordering': ['-class_session__date', '-class_session__start_time'],
                'unique_together': {('student', 'class_session')},
            },
        ),
    ]
