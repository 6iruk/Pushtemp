from django.db import models

class PushPage(models.Model):
   event = models.CharField(max_length=50)
   template = models.CharField(max_length=150)

   def __str__(self):
      return self.event

#   def get_link_one(self):
#      return 'Push_Page/' + self.img1.url.split('/')[-1]

class Post(models.Model):
   content = models.TextField(blank=True)
   pub_date = models.DateTimeField('Post date')
   page = models.ForeignKey(PushPage, on_delete=models.CASCADE)

   def __str__(self):
      return self.content

def upload_path(instance,filename):
   return 'Push_Page/static/' + filename

class Picture(models.Model):
   image = models.FileField(upload_to=upload_path)
   description = models.TextField(blank=True)
   content = models.ForeignKey(Post,  on_delete=models.CASCADE)
