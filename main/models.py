from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
from main.models import *
import math

## ENTITES ##

class Educational_Institution(models.Model):

   #Possible values for the 'ownership_type' field
   ownership_type_choices = (
      ('pvt','Private'),
      ('pbc','Public'),
      ('gvt','Government'),
   )

   #Possible values for the 'institution_type' field
   institution_type_choices = (
      ('clg','College'),
      ('uni','University'),
   )

   #The name of the institution
   name = models.CharField(max_length=100)

   #The country the institution is based in
   country = models.CharField(max_length=50)

   #The city the institution is based in
   city = models.CharField(max_length=50)

   #The type of ownership of the institution
   ownership_type = models.CharField(max_length=50, choices=ownership_type_choices)

   #The type of institution of the institution
   institution_type = models.CharField(max_length=50, choices=institution_type_choices)


   def __str__(self):
      return self.name



## After this comment the word 'Institution' will be replaced with 'University' for the sake of simplicity


class Department(models.Model):

   #The university the department is in
   university_in = models.ForeignKey(Educational_Institution, on_delete=models.CASCADE)

   #The name of the department
   name = models.CharField(max_length=60)

   #The academic discipline/field the department is concerned with
   field = models.CharField(max_length=20)

   def __str__(self):
      return self.name

   def get_classes(self):
       x = Q()

       for course in self.course_set.all():
           x = x | Q(section_takes = course)

       temp_sections = Section.objects.filter(x).order_by('department_in')
       ids = temp_sections.values_list('department_in__id', flat=True).distinct()

       sections = []

       for id in ids:
           sections.append(list(temp_sections.filter(department_in__id = id).order_by('department_in','year','section_id').distinct()))

       return sections


class Section(models.Model):

   #The department the section is in
   department_in = models.ForeignKey(Department, on_delete=models.CASCADE)

   #The year the section is in
   year = models.IntegerField()

   #The section number/alphabet of the section
   section_id = models.CharField(max_length=2)

   #The courses taken by this section
   section_takes = models.ManyToManyField('Course')

   def __str__(self):
      return self.department_in.name + '-' + str(self.year) + '-' + self.section_id  ##correct this - output as a long string



class Course(models.Model):

  #The name of the course
   name = models.CharField(max_length=100)

   #The course code of the course
   course_code = models.CharField(max_length=20, null=True, blank=True)

   #The module code of the course
   module_code = models.CharField(max_length=20, null=True, blank=True)

   #The department that gives this course
   given_by = models.ForeignKey(Department, on_delete=models.CASCADE)

   def __str__(self):
      return self.name

   #Returns the name of the course after replacing the spaces ' ' with underscores '_'. This is used when using the course name in the URL.
   def get_link_name(self):
        return self.name.replace(' ', '_')



#The upload path for a file
def upload_path_file(instance, filename):
   return 'File' + '/' + instance.post_by.department_in.university_in.name + '/' + instance.post_by.department_in.name + '/' + instance.post_by.title + instance.post_by.first_name + " " + instance.post_by.last_name + '/' + instance.name + '.' +  instance.extension



#The upload path for an image
def upload_path_image(instance, filename):
   return 'Image' + '/' + instance.post_by.department_in.university_in.name + '/' + instance.post_by.department_in.name + '/' + instance.post_by.title + instance.post_by.first_name + " " + instance.post_by.last_name + '/' + filename



class File(models.Model):

   #The content of the file
   file = models.FileField(upload_to=upload_path_file, max_length=300)

   #The name of the file
   name = models.CharField(max_length=20)

   #The extension of the file
   extension = models.CharField(max_length=8)

   #The staff member that uploaded the file
   post_by = models.ForeignKey('Staff',  on_delete=models.CASCADE)

   def __str__(self):
      return self.name

   def downloads(self):
      count = self.download_set.count()

      return count

class Image(models.Model):

   #The content of the image
   image = models.FileField(upload_to=upload_path_image, max_length=300)

   #The staff member that uploaded the image
   post_by = models.ForeignKey('Staff',  on_delete=models.CASCADE)

   def __str__(self):
      return self.image.name


class Post(models.Model):

   #The content of the post
   content = models.TextField()

   #The files attached to the post
   files = models.ManyToManyField(File, blank=True)

   #The images attached to the post
   images = models.ManyToManyField(Image, blank=True)  ##did you mean to name this 'images'?

   #The type of the post. Notice = 1, Announcement = 2, Specific = 3, Group Message = 4, Staff Message = 5.
   post_type = models.IntegerField()

   #The staff member that posted the post
   post_by = models.ForeignKey('Staff',  on_delete=models.CASCADE)

   #The date and time the post was posted
   pub_date = models.DateTimeField('Date Published')

   def __str__(self):
      return self.content

   def delivered(self):
      count = self.tracking_set.count()

      return count

   def read(self):
      count = self.tracking_set.filter(status=2).count()

      return count

   def is_read(self):
      count = models.Tracking.objects.filter(student = student, post = post, status = 1).count()

      return count

   def recipients_string(self):
      recipients = ""
      for recipient in self.post_to_class_set.all():
        recipients += recipient.recipient()

      return recipients

class Reminder(models.Model):

   #The type of the reminder. Test = 1, Assignment = 2, Presentation = 3
   reminder_for = models.IntegerField()

   #The title of the reminder Eg.Test II, Assignment 1
   title = models.CharField(max_length=20)

   #The note for the test,assignment or presentation
   note = models.TextField(blank=True)

   #The due date of the test,assignment or presentation
   due_date = models.DateTimeField()

   #The due time of the test,assignment or presentation
   due_time = models.DateTimeField()

   #The place where the test,assignment submission or presentation will occur
   place = models.CharField(max_length=20)

   def __str__(self):
      return self.title



## ACTORS ##

class Staff(models.Model):

   #Possible values for the title field
   title_choices = (
      ('Mr.','Mr.'),
      ('Ms.','Ms.'),
      ('Mrs.','Mrs.'),
      ('Dr.','Doctor'),
      ('Prof.','Professor')
   )

   #Possible values for the role field
   role_choices = (
      ('Dean','Dean'),
      ('Associate Dean','Associate Dean'),
      ('Registrar','Registrar'),
      ('Department Head','Department Head'),
      ('Program Coordinator','Program Coordinator'),
      ('Instructor','Instructor'),
      ('Lab Technician','Lab Technician')  # how about we just use instructor
   )

   #The university the staff member is in
   university_in = models.ForeignKey(Educational_Institution,  on_delete=models.CASCADE)

   #The department the staff member is in
   department_in = models.ForeignKey(Department,  on_delete=models.CASCADE)

   #The title of the staff member
   title = models.CharField(max_length=15, choices=title_choices)

   #The first name of the staff member
   first_name = models.CharField(max_length=50)

   #The last name of the staff member
   last_name = models.CharField(max_length=50)

   #The phone number of the staff member
   phone = models.CharField(max_length=20)   #optional?

   #The email of the staff member
   email = models.EmailField(max_length=254, null=True)  #must be mandatory

   #The role of the staff member
   role = models.CharField(max_length=15, choices=role_choices)   #this shouldn't be the option for the user

   #The user object associated with this staff member
   user = models.OneToOneField(User,  on_delete=models.CASCADE)

   #staff_id = models.CharField(max_length=50, null=True)  # we need the staff ID

   def __str__(self):
      return self.title + " " + self.first_name  #also add the staff ID here so it's easy to debug

   def get_classes(self):
      department_ids = self.instructor_teaches_set.values_list('section__department_in__id', flat=True).distinct()
      classes = []

      for id in department_ids:
          classes.append(list(self.instructor_teaches_set.filter(section__department_in__id = id)))

      return classes


class Student(models.Model):

   #The university the student is in
   university_in = models.ForeignKey(Educational_Institution, on_delete=models.CASCADE)

   #The department the student is in
   department_in = models.ForeignKey(Department,  on_delete=models.CASCADE)

   #The year the student is in
   year = models.IntegerField()   #add section field here?

   #The year the student is in
   section = models.CharField(max_length=5)

   #The first name of the student
   first_name = models.CharField(max_length=50)

   #The last name of the student
   last_name = models.CharField(max_length=50)

   #The registration ID of the student
   reg_id = models.CharField(max_length=20)

   #The phone number of the student
   phone = models.CharField(max_length=20)

   #The email of the student
   email = models.EmailField(max_length=254, null=True)

   #The telegram chat id of the student
   chat_id = models.IntegerField(default=0)

   #The user object associated with this student
   user = models.OneToOneField(User,  on_delete=models.CASCADE)

   #The classes the student takes
   class_in = models.ManyToManyField('Instructor_Teaches')

   def __str__(self):
      return self.reg_id



## RELATIONSHIPS ##

#A lecturer teaches a certain course to a section
class Instructor_Teaches(models.Model):

   #The lecturer that teaches
   instructor = models.ManyToManyField(Staff)

   #The section the lecturer teaches
   section = models.ForeignKey(Section,  on_delete=models.CASCADE)

   #The course the lecturer teaches to the section
   course = models.ForeignKey(Course,  on_delete=models.CASCADE)

   def __str__(self):
      return str(self.section.year) + "-" + self.course.name



#An instructor posts to a class
class Post_To_Class(models.Model):

   #The class the post is intended for
   post_to = models.ForeignKey(Instructor_Teaches,  on_delete=models.CASCADE)

   #The post
   post = models.ForeignKey(Post,  on_delete=models.CASCADE)

   def __str__(self):
      return str(self.post.post_by) + "-" + str(self.post_to)

   def recipient(self):
      return self.post_to.section.department_in.name + " Year " + str(self.post_to.section.year) + " Section " + self.post_to.section.section_id + " - " + self.post_to.course.name

#A staff member posts to a section
class Post_To_Section(models.Model):

   #The section the post is intended for
   post_to = models.ForeignKey(Section,  on_delete=models.CASCADE)

   #The post
   post = models.ForeignKey(Post,  on_delete=models.CASCADE)

   def __str__(self):
      return str(self.post.post_by) + "-" + str(self.post_to)

   def recipient(self):
      return self.post_to.department_in.name + " Year " + str(self.post_to.year) + " Section " + self.post_to.section_id


#A staff member posts to a student
class Post_To_Student(models.Model):

   #The student the post is intended for
   post_to = models.ForeignKey(Student,  on_delete=models.CASCADE)

   #The post
   post = models.ForeignKey(Post,  on_delete=models.CASCADE)

   def __str__(self):
      return str(self.post.post_by) + "-" + str(self.post_to)



#A staff member posts to a group chat
class Post_To_Chat(models.Model):

   #The group chat the post is intended for
   post_to = models.ForeignKey(Department,  on_delete=models.CASCADE)

   #The post
   post = models.ForeignKey(Post,  on_delete=models.CASCADE)

   def __str__(self):
      return str(self.post.post_by) + "-" + str(self.post_to)



#A staff member posts to a staff member
class Post_To_Staff(models.Model):

   #The staff member the post is intended for
   post_to = models.ForeignKey(Staff,  on_delete=models.CASCADE)

   #The post
   post = models.ForeignKey(Post,  on_delete=models.CASCADE)

   def __str__(self):
      return str(self.post.post_by) + "-" + str(self.post_to)


#An Instructor sets a reminder for a class
class Reminder_To_Class(models.Model):

    #The class the reminder is intended for
    reminder_to = models.ForeignKey(Instructor_Teaches,  on_delete=models.CASCADE)

    #The reminder
    reminder = models.ForeignKey(Reminder,  on_delete=models.CASCADE)



## TRACKING ##

#A student received/read a post
class Tracking(models.Model):

   #The student that received/read the post
   student = models.ForeignKey(Student,  on_delete=models.CASCADE)

   #The post
   post = models.ForeignKey(Post,  on_delete=models.CASCADE)

   #Post status. Delivered = 1, Read = 2
   status = models.IntegerField()

   #The delivery date/time
   del_on = models.DateTimeField('Delivery On')

   #The date/time the post was read
   read_on = models.DateTimeField('Read On', null= True, blank=True)

   def __str__(self):
      return str(self.post.id) + "-" + self.student.reg_id



class Download(models.Model):

   #The student that downlaads the file
   student = models.ForeignKey(Student, on_delete=models.CASCADE)

   #The file
   file = models.ForeignKey(File,  on_delete=models.CASCADE)

   #Download status. True = Download finished
   status = models.BooleanField(default=False)

   #The download date/time
   start = models.DateTimeField('Started On')

   #The time the download finished
   finish = models.DateTimeField('Finished On', null= True, blank=True)

   def __str__(self):
      return str(self.file.id) + "-" + self.student.reg_id



##class Announcement(models.Model):
##   pub_date = models.DateTimeField('Date Published')
##   exp_date = models.DateTimeField('Expiry Date')
##   message  = models.TextField()
##   count = models.IntegerField()
##
##   def __str__(self):
##      return str(self.pub_date)
##
##   def inc_count(self):
##      self.count = self.count + 1
##      self.save()
##      return True
##
##def upload_path(instance, filename):
##   return instance.teacher.department.university.code + '/' + instance.teacher.department.dept_code + '/' + instance.teacher.title + instance.teacher.first_name + '/' + instance.name + '.' +  instance.ext()
##
##class Material(models.Model):
##   name = models.CharField(max_length=50)
##   description = models.TextField()
##   file = models.FileField(upload_to=upload_path, max_length=300)
##   pub_date = models.DateTimeField('Date Published')
##   teacher = models.ForeignKey(Teacher , null= True)
##   count = models.IntegerField()
##
##   class Meta:
##      get_latest_by = "pub_date"
##
##   def __str__(self):
##      return self.name
##
##   def ext (self):
##      return self.file.name.split('.')[-1]
##
##   def file_size(self):
##      size_bytes = self.file.size
##      i = float(size_bytes/1024)
##      return i
##
##   def inc_count(self):
##      self.count = self.count + 1
##      self.save()
##      return True
##
##class Material_To(models.Model):
##   to = models.ForeignKey(Teacher_Teaches)
##   material = models.ForeignKey(Material)
##   pub_date = models.DateTimeField('Date Published', null= True)
##
##class Announcement_To(models.Model):
##   to = models.ForeignKey(Teacher_Teaches)
##   announcement = models.ForeignKey(Announcement)
##   pub_date = models.DateTimeField('Date Published', null= True)
##
