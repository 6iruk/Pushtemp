from django.db import models
from main.models import *

# Create your models here.


class Forum(models.Model):
    # The name of the forum
    name = models.CharField(max_length=120)

    # A description about the kind of topics discussed in the forum
    description = models.TextField(blank=False)

    # A unique id that users could check to identify the forum
    forum_id = models.CharField(max_length=40)

    # The forums privacy flag
    privacy = models.BooleanField(default=False)

    # The join code for the forum
    join_code = models.CharField(max_length=8)

    # The restrictions on the forum
    restrictions = models.ManyToManyField('ForumRestriction', blank=True)

    # The creator of the forum
    creator = models.OneToOneField(User, on_delete=models.CASCADE)

    # The restrictions on the forum
    members = models.ManyToManyField(User, blank=True, related_name='+')

    def __str__(self):
        return self.name


class ForumRestriction(models.Model):
    # The department that a forum is allowed for
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    # The year that a forum is allowed for
    year = models.IntegerField()

    # The section that a forum is allowed for
    section = models.ForeignKey(Section, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
