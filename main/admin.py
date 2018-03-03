from django.contrib import admin
from .models import *

# Register your models here.
models = [University, Department, Course, Section, Teacher, Teacher_Teaches, Announcement, Material, Announcement_To, Material_To]

for model in models:
	admin.site.register(model)
