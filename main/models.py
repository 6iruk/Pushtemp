from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
import math

class University(models.Model):
   country = models.CharField(max_length=50)
   city = models.CharField(max_length=50)
   name = models.CharField(max_length=100)
   code = models.CharField(max_length=20)

   def __str__(self):
      return self.name
   
class Department(models.Model):
   university = models.ForeignKey(University)
   name = models.CharField(max_length=60)
   dept_code = models.CharField(max_length=20)
   code = models.CharField(max_length=41)
  
   def __str__(self):
      return self.name
   
class Course(models.Model):
   name = models.CharField(max_length=100)
   module_code = models.CharField(max_length=20)
   course_code = models.CharField(max_length=20)
   department = models.ForeignKey(Department)
   code = models.CharField(max_length=62)
   
   def __str__(self):
      return self.name

   def get_link_name(self):
        return self.name.replace(' ', '_')

class Section(models.Model):
   year = models.IntegerField()
   number = models.IntegerField()
   department = models.ForeignKey(Department)
   code = models.CharField(max_length=50)
   take = models.ManyToManyField(Course)
   
   def __str__(self):
      return self.code

class Teacher(models.Model):
   title_choices = (
      ('Mr.','Mr.'),
      ('Ms.','Ms.'),
      ('Mrs.','Mrs.'),
      ('Dr.','Doctor'),
      ('Prof.','Professor')
   )

   title = models.CharField(max_length=15, choices=title_choices)
   user = models.OneToOneField(User)
   first_name = models.CharField(max_length=50)
   last_name = models.CharField(max_length=50)
   email = models.EmailField(max_length=254)
   department = models.ForeignKey(Department)

   def __str__(self):
      return self.title + " " + self.first_name

class Teacher_Teaches(models.Model):
   teacher = models.ForeignKey(Teacher)
   section = models.ForeignKey(Section)
   course = models.ForeignKey(Course)

   def __str__(self):
      return self.teacher.first_name + "-" + self.section.code + "-" + self.course.name
   
class Announcement(models.Model):
   pub_date = models.DateTimeField('Date Published')
   exp_date = models.DateTimeField('Expiry Date')
   message  = models.TextField()
   count = models.IntegerField()

   def __str__(self):
      return str(self.pub_date)
    
   def inc_count(self):
      self.count = self.count + 1
      self.save()
      return True

def upload_path(instance, filename):
   return instance.teacher.department.university.code + '/' + instance.teacher.department.dept_code + '/' + instance.teacher.title + instance.teacher.first_name + '/' + instance.name + '.' +  instance.ext()

class Material(models.Model):
   name = models.CharField(max_length=50)
   description = models.TextField()    
   file = models.FileField(upload_to=upload_path, max_length=300)
   pub_date = models.DateTimeField('Date Published')
   teacher = models.ForeignKey(Teacher , null= True)
   count = models.IntegerField()

   class Meta:    
      get_latest_by = "pub_date"

   def __str__(self):
      return self.name
    
   def ext (self):
      return self.file.name.split('.')[-1]
    
   def file_size(self):
      size_bytes = self.file.size
      i = float(size_bytes/1024)
      return i
    
   def inc_count(self):
      self.count = self.count + 1
      self.save()
      return True

class Material_To(models.Model):
   to = models.ForeignKey(Teacher_Teaches)
   material = models.ForeignKey(Material)

class Announcement_To(models.Model):
   to = models.ForeignKey(Teacher_Teaches)
   announcement = models.ForeignKey(Announcement)
