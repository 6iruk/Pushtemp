from django.contrib import admin
from .models import *

# Register your models here.
models = [Educational_Institution, Department, Section, Course, File, Image, Post, Reminder, Staff, Student, Instructor_Teaches, Post_To_Class, Post_To_Section, Post_To_Student, Post_To_Chat, Post_To_Staff, Reminder_To_Class, Tracking]

for model in models:
	admin.site.register(model)
