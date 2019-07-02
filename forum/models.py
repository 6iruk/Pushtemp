from main.models import *

# Create your models here.

def upload_path_file(instance, filename):
    if Staff.objects.filter(user=instance.post_by).exists():
        staff = Staff.objects.get(user=instance.post_by)

        return 'Image' + '/' + staff.department_in.university_in.name + '/' + staff.department_in.name + '/' + staff.title + staff.first_name + " " + staff.last_name + '/' + instance.name + '.' +  instance.extension

    elif Student.objects.filter(user=instance.post_by).exists():
        student = Student.objects.get(user=instance.post_by)

        return 'Image' + '/' + 'students' + '/' +  student.reg_id + instance.name + '.' +  instance.extension

class Forum(models.Model):
    # The name of the forum
    name = models.CharField(max_length=120)

    #The forum photo/picture
    file = models.FileField(upload_to=upload_path_file, max_length=300)

    # A description about the kind of topics discussed in the forum
    description = models.TextField(blank=False)

    # A unique id that users could check to identify the forum
    forum_id = models.CharField(max_length=40)

    # The forums privacy flag
    privacy = models.BooleanField(default=False)

    # The join code for the forum
    join_code = models.CharField(max_length=8, blank=True)

    # The restrictions on the forum
    restrictions = models.ManyToManyField('ForumRestriction', blank=True)

    # The creator of the forum
    creator = models.OneToOneField(User, on_delete=models.CASCADE)

    # The restrictions on the forum
    members = models.ManyToManyField(User, blank=True, related_name='+')

    # The posts of the forum
    posts = models.ManyToManyField(Post, blank=True, related_name='+')

    def __str__(self):
        return self.name


class ForumRestriction(models.Model):
    # The department that a forum is allowed for
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    # The year that a forum is allowed for
    year = models.IntegerField(blank=True)

    # The section that a forum is allowed for
    section = models.ForeignKey(Section, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return self.name
