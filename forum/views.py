from django.shortcuts import render
from forum.models import *
from django.http import HttpResponse, JsonResponse
import datetime, zipfile, io

# Create your views here.


def forum_home(request):

    return render(request, 'forum/forum_home.html')


def forum_create(request):

    return render(request, 'forum/forum_create.html')


def forum_feed(request):

    return render(request, 'forum/forum_feed.html')


def forum_search(request):

    return render(request, 'forum/forum_search.html')


# ------------------------------------------------------------
# Forum API
# ------------------------------------------------------------


def forums_user_is_in(request):

    forums = Forum.objects.filter(members = request.user)

    #JSON output
    #Start json array
    output = "["

    # Loop through every Forum and add them as a json object
    for forum in forums:
        output += "{"
        output += "\"id\":" + str(forum.id) + ","
        output += "\"name\":" + "\"" + forum.name + "\"" + ","
        output += "\"description\":" + "\"" + forum.description + "\"" + ","
        output += "\"forum_id\":" + "\"" + forum.forum_id + "\"" + ","
        output += "\"privacy\":" + "\"" + str(forum.privacy) + "\""
        output += "},"

    # remove the last list separator comma
    output = output[::-1].replace(",", "", 1)[::-1]

    #end of json array
    output += "]"

    return HttpResponse(output, content_type='application/json')


def trending_forums(request):

    forums = Forum.objects.all()

    #JSON output
    #Start json array
    output = "["

    # Loop through every Forum and add them as a json object
    for forum in forums:
        output += "{"
        output += "\"id\":" + str(forum.id) + ","
        output += "\"name\":" + "\"" + forum.name + "\"" + ","
        output += "\"description\":" + "\"" + forum.description + "\"" + ","
        output += "\"forum_id\":" + "\"" + forum.forum_id + "\"" + ","
        output += "\"privacy\":" + "\"" + str(forum.privacy) + "\""
        output += "},"

    # remove the last list separator comma
    output = output[::-1].replace(",", "", 1)[::-1]

    #end of json array
    output += "]"

    return HttpResponse(output, content_type='application/json')


def forum_posts(request):

    forum = Forum.objects.get(id = int(request.GET.get('forum-id')))

    #JSON output
    #Start json array
    output = "["

    # Loop through every Post and add them as a json object
    for Post in forum.posts.order_by('-pub_date'):
        output += "{"
        output += "\"id\":" + "\"" + str(Post.id) + "\"" + ","
        output += "\"content\":" + "\"" + Post.content + "\"" + ","

        #Start json array for Post files
        output += "\"files\":" + "["

        for File in Post.files.all():
            output += "{"
            output += "\"id\":" + "\"" + str(File.id) + "\"" + ","
            output += "\"name\":" + "\"" + File.name + "\"" + ","
            output += "\"extension\":" + "\"" + File.extension + "\"" + ","
            output += "\"post_by\":" + "\"" + File.post_by.__str__() + "\""
            output += "},"

        if Post.files.all().count() > 0:
            # remove the last list separator comma
            output = output[::-1].replace(",", "", 1)[::-1]

        #Close files array
        output += "],"

        #Start json array for Post images
        output += "\"images\":" + "["

        for Image in Post.images.all():
            output += "{"
            output += "\"id\":" + "\"" + str(Image.id) + "\"" + ","
            output += "\"post_by\":" + "\"" + Image.post_by.__str__() + "\""
            output += "},"

        if Post.images.all().count() > 0:
            # remove the last list separator comma
            output = output[::-1].replace(",", "", 1)[::-1]

        #Close images array
        output += "],"

        output += "\"post_type\":" + "\"" + str(Post.post_type) + "\"" + ","
        output += "\"post_by\":" + "\"" + Post.post_by.__str__() + "\"" + ","
        output += "\"pub_date\":" + "\"" + str(Post.pub_date)+ "\"" 
        output += "},"

    # remove the last list separator comma
    output = output[::-1].replace(",", "", 1)[::-1]

    #end of json array
    output += "]"

    return HttpResponse(output, content_type='application/json')


def send_message(request):
    if request.POST.get('content').strip() == "":
        return HttpResponse("{\"status\":0, \"remark\":\"Content not found\"}", content_type='application/json')

    if request.FILES.get('file-1'):
        if request.POST.get('file-name-1').strip() == "":
            return HttpResponse("{\"status\":0, \"remark\":\"File name not found\"}", content_type='application/json')

    if request.FILES.get('image-1'):
        if request.FILES['image-1'].name.split('.')[-1].strip().lower() not in ["jpeg","jpg","gif","png","bmp","svg"]:
            return HttpResponse("{\"status\":0, \"remark\":\"Image format not supported\"}", content_type='application/json')

    if request.FILES.get('image-2'):
        if request.FILES['image-2'].name.split('.')[-1].strip().lower() not in ["jpeg","jpg","gif","png","bmp","svg"]:
            return HttpResponse("{\"status\":0, \"remark\":\"Image format not supported\"}", content_type='application/json')

    content = request.POST.get('content')
    pub_date = datetime.datetime.now()

    post = Post.objects.create(content = content, post_type = 6, post_by = request.user, pub_date = pub_date)

    if request.FILES.get('file-1'):
        name = request.POST.get('file-name-1')
        file = models.File.objects.create(file = request.FILES.get('file-1'), name = name, extension = request.FILES['file-1'].name.split('.')[-1], post_by = request.user)
        post.files.add(file)

    if request.FILES.get('image-1'):
        file = models.Image.objects.create(image = request.FILES['image-1'], post_by = request.user)
        post.images.add(file)

    if request.FILES.get('image-2'):
        file = models.Image.objects.create(image = request.FILES['image-2'], post_by = request.user)
        post.images.add(file)

    forum = Forum.objects.get(id = int(request.POST.get('forum_id')))
    forum.posts.add(post)

    return HttpResponse("{\"status\":1, \"remark\":\"Post successful\"}", content_type='application/json')


def join_forum(request):
    forum = Forum.objects.get(id = int(request.GET.get('forum-id')))
    forum.members.add(request.user)

    return HttpResponse("{\"status\":1, \"remark\":\"User joined the forum\"}", content_type='application/json')

#join closed forum. Takes 'code',  /forum/joinclosedforum/

#create forum   /forum/createforum/
# forum-name
# forum-description
# thumbnail
# departments
# joincode

#search forum   /forum/search/
# query

#Assignment Functions
#set assignment /setassignment/
# assignment-name
# file
# due_date
# class-recipients
# comment (optional)

#assignmentlist /assignmentlist/
# assignment-name
# accepting: true or false
# description
# due_date

#assignment submissions /getsubmissions/
#I will send assignment-id
# student-name
# student-id
# comment
# file

def leave_forum(request):
    forum = Forum.objects.get(id = int(request.GET.get('forum-id')))
    forum.members.remove(request.user)

    return HttpResponse("{\"status\":1, \"remark\":\"User left the forum\"}", content_type='application/json')


def delete_forum(request):
    #verify if user is the creator
    forum = Forum.objects.get(id = int(request.GET.get('forum-id')))
    forum.delete()

    return HttpResponse("{\"status\":1, \"remark\":\"Forum deleted\"}", content_type='application/json')