from django.shortcuts import render
from main import models
from forum import models as forum_models
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User
import random
import datetime
from django.db.models import Q


def login(request):

    if request.POST.get('user-type') == 'staff':
        if not request.POST.get('email') or request.POST.get('email').strip() == "":
            return HttpResponse("{\"success\":0, \"userToken\":\"\"}", content_type='application/json')

        if not request.POST.get('password') or request.POST.get('password').strip() == "":
            return HttpResponse("{\"success\":0, \"userToken\":\"\"}", content_type='application/json')

        staff = models.Staff.objects.get(email = request.POST.get('email'))
        password = request.POST.get('password')
        user = authenticate(username=staff.user.username, password=password)

    elif request.POST.get('user-type') == 'student':
        if not request.POST.get('reg-id') or request.POST.get('reg-id').strip() == "":
            return HttpResponse("{\"success\":0, \"userToken\":\"\"}", content_type='application/json')
        if not request.POST.get('password') or request.POST.get('password').strip() == "":
            return HttpResponse("{\"success\":0, \"userToken\":\"\"}", content_type='application/json')
        if not models.Student.objects.filter(reg_id = request.POST.get('reg-id')).exists():
            return HttpResponse("{\"success\":0, \"userToken\":\"\"}", content_type='application/json')

        student = models.Student.objects.get(reg_id = request.POST.get('reg-id'))
        password = request.POST.get('password')
        user = authenticate(username=student.user.username, password=password)

    else:
        return HttpResponse("{\"success\":0, \"userToken\":\"\"}", content_type='application/json')

    if user is not None:
        if user.is_active:
            token = "tok" + str(random.randint(1000, 99999999))

            while User.objects.filter(first_name = token).exists():
                token = "tok" + str(random.randint(1000, 99999999))

            user.first_name = token
            user.save()

            return HttpResponse("{\"success\":1, \"userToken\":\"" + user.first_name + "\"}", content_type='application/json')
        else:
            return HttpResponse("{\"success\":0, \"userToken\":\"\"}", content_type='application/json')
    else:
        return HttpResponse("{\"success\":0, \"userToken\":\"\"}", content_type='application/json')


def signup(request):

    if not request.POST.get('firstname') or (request.POST.get('firstname').strip() == ""):
        return HttpResponse("{\"success\":0, \"error\":\"First name required\", \"userToken\":\"\"}", content_type='application/json')

    if not request.POST.get('lastname') or (request.POST.get('lastname').strip() == ""):
        return HttpResponse("{\"success\":0, \"error\":\"Last name required\", \"userToken\":\"\"}", content_type='application/json')

    if not request.POST.get('phone') or (request.POST.get('phone').strip() == ""):
        return HttpResponse("{\"success\":0, \"error\":\"Phone number required\", \"userToken\":\"\"}", content_type='application/json')

    if not request.POST.get('phone').startswith("09") and not request.POST.get('phone').startswith("251") and not request.POST.get('phone').startswith("+251"):
        return HttpResponse("{\"success\":0, \"error\":\"Phone number format not correct\", \"userToken\":\"\"}", content_type='application/json')

    if not request.POST.get('phone').isdigit():
        return HttpResponse("{\"success\":0, \"error\":\"Phone number format not correct\", \"userToken\":\"\"}", content_type='application/json')

    if request.POST.get('email') and request.POST.get('email').strip() != "":
        e = request.POST.get('email')
        if e.strip().rfind('.') == -1 or e.strip().rfind('@') == -1 or (e.strip().rfind('.') <= e.strip().rfind('@')):
            return HttpResponse("{\"success\":0, \"error\":\"Email not valid\", \"userToken\":\"\"}", content_type='application/json')

    if not request.POST.get('department') or not models.Department.objects.filter(id = int(request.POST.get('department'))).exists():
        return HttpResponse("{\"success\":0, \"error\":\"Valid Department ID required\", \"userToken\":\"\"}", content_type='application/json')

    if not request.POST.get('year') or (request.POST.get('year').strip() == "") :
        return HttpResponse("{\"success\":0, \"error\":\"Year required\", \"userToken\":\"\"}", content_type='application/json')

    if not request.POST.get('year').split('-')[-1].isdigit() or not models.Section.objects.filter(department_in = models.Department.objects.get(id = int(request.POST.get('department'))), year = int(request.POST.get('year').split('-')[-1])).exists():
        return HttpResponse("{\"success\":0, \"error\":\"Year doesn't exist\", \"userToken\":\"\"}", content_type='application/json')

    if not request.POST.get('section') or request.POST.get('section').strip() == "":
        return HttpResponse("{\"success\":0, \"error\":\"Section required\", \"userToken\":\"\"}", content_type='application/json')

    if not models.Section.objects.filter(department_in = models.Department.objects.get(id = int(request.POST.get('department'))), year = int(request.POST.get('year').split('-')[-1]), section_id = request.POST.get('section')).exists():
        return HttpResponse("{\"success\":0, \"error\":\"Section not found\", \"userToken\":\"\"}", content_type='application/json')

    if not request.POST.get('reg_id') or (request.POST.get('reg_id').strip() == ""):
        return HttpResponse("{\"success\":0, \"error\":\"Registration ID required\", \"userToken\":\"\"}", content_type='application/json')

    if len(request.POST.get('reg_id').split('/')) != 3 or request.POST.get('reg_id').split('/')[0].upper() != "NSR" or not request.POST.get('reg_id').split('/')[1].isdigit() or not request.POST.get('reg_id').split('/')[2].isdigit():
        return HttpResponse("{\"success\":0, \"error\":\"ID not correct\", \"userToken\":\"\"}", content_type='application/json')

    if User.objects.filter(username = request.POST.get('reg_id').replace("/","-")).exists():
        return HttpResponse("{\"success\":0, \"error\":\"ID already in use\", \"userToken\":\"\"}", content_type='application/json')

    if not request.POST.get('password') or (request.POST.get('password').strip() == "") or len(request.POST.get('password')) < 7:
        return HttpResponse("{\"success\":0, \"error\":\"Password must contain more than 7 letters and/or numbers\", \"userToken\":\"\"}", content_type='application/json')

    first_name = request.POST.get('firstname')
    last_name = request.POST.get('lastname')
    phone = request.POST.get('phone')

    if request.POST.get('email'):
        email = request.POST.get('email')

    else:
        email = ""

    department_in = models.Department.objects.get(id = int(request.POST.get('department')))
    year = int(request.POST.get('year').split('-')[-1])
    section = models.Section.objects.get(department_in = department_in, year = year, section_id = request.POST.get('section'))
    reg_id = request.POST.get('reg_id')
    password = request.POST.get('password')

    user = User.objects.create_user(reg_id.replace("/","-"), "", password)
    student = models.Student.objects.create(university_in = department_in.university_in, department_in = department_in, year = year, section = section.section_id, first_name = first_name, last_name = last_name, reg_id = reg_id, phone = phone, email = email, user = user)

    for course in section.section_takes.all():
        if not models.Instructor_Teaches.objects.filter(section = section, course = course).exists():
            models.Instructor_Teaches.objects.create(section = section, course = course)

        class_in = models.Instructor_Teaches.objects.get(section = section, course = course)
        student.class_in.add(class_in)

    token = "tok" + str(random.randint(1000, 99999999))

    while User.objects.filter(first_name = token).exists():
        token = "tok" + str(random.randint(1000, 99999999))

    user.first_name = token
    user.save()

    return HttpResponse("{\"success\":1, \"error\":\"\", \"userToken\":\"" + user.first_name + "\"}", content_type='application/json')


def your_wall_post(request):

    token = request.POST.get('userToken')

    if User.objects.filter(first_name = token).exists():
        student = models.Student.objects.get(user__first_name = token)

    else:
        return HttpResponse("{\"success\":0, \"error\":\"Invalid user token\", \"userToken\":\"\"}", content_type='application/json')

    #Get the classes the student takes part in
    classes_in = student.class_in.all()

    #A query to filter posts
    query = Q()

    #Loop through the classes the student takes to build a query
    for class_in in classes_in:

        #Add every class the student takes to the query
        query.add( Q( post_to = class_in ), Q.OR )

    posts_to_class = models.Post_To_Class.objects.filter( post__id__gt = int(request.POST.get('latestPostId'))).filter(query)

    posts_to_student = models.Post_To_Student.objects.filter( post__id__gt = int(request.POST.get('latestPostId'))).filter(post_to = student)

    posts = sorted((list(posts_to_class) + list(posts_to_student)), key=lambda x: x.post.pub_date)


    #JSON output
    #Start json array
    output = "{"
    output += "posts: ["

    # Loop through every Post and add them as a json object
    for Post in posts:
        staff = models.Staff.objects.get(user=Post.post.post_by)

        if not models.Tracking.objects.filter(student = student, post = Post.post).exists():
            models.Tracking.objects.create(student = student, post = Post.post, status = 1, del_on = datetime.datetime.now())

        output += "{"
        output += "\"id\":" + str(Post.post.id) + ","
        output += "\"content\":" + "\"" + Post.post.content + "\"" + ","
        output += "\"read\":" + str(models.Tracking.objects.filter(student = student, post = Post.post, status = 2).exists()) + ","

        #Start json array for Post files
        output += "\"files\":" + "["

        for File in Post.post.files.all():
            output += "{"
            output += "\"id\":" + str(File.id) + ","
            output += "\"name\":" + "\"" + File.name + "\"" + ","
            output += "\"extension\":" + "\"" + File.extension + "\"" + ","
            output += "\"size\":" + "\"" + File.file.size + "\"" + ","
            output += "\"uri\":\"/media/" + File.file + "\""
            output += "},"

        if Post.post.files.all().count() > 0:
            # remove the last list separator comma
            output = output[::-1].replace(",", "", 1)[::-1]

        #Close files array
        output += "],"

        #Start json array for Post images
        output += "\"images\":" + "["

        for Image in Post.post.images.all():
            output += "{"
            output += "\"id\":" + str(Image.id) + ","
            output += "\"uri\":\"/media/" + Image.image + "\""
            output += "},"

        if Post.post.images.all().count() > 0:
            # remove the last list separator comma
            output = output[::-1].replace(",", "", 1)[::-1]

        #Close images array
        output += "],"

        output += "\"post_by\":" + "\"" + staff.__str__() + "\"" + ","
        output += "\"post_course\":" + "\"" + Post.post_to.course.name + "\"" + ","
        output += "\"post_courseid\":" + str(Post.post_to.course.id) + ","
        output += "\"pub_date\":" + "\"" + str(Post.post.pub_date) + "\""
        output += "},"

    # remove the last list separator comma
    output = output[::-1].replace(",", "", 1)[::-1]

    #end of json array
    output += "],"
    output += "\"latestPostId\":" + str(posts[0].id) + ","
    output += "}"

    return HttpResponse(output, content_type='application/json')


def student_click_read(request):
    token = request.POST.get('userToken')

    if User.objects.filter(first_name = token).exists():
        student = models.Student.objects.get(user__first_name = token)

    else:
        return HttpResponse("{\"success\":0, \"error\":\"Invalid user token\", \"userToken\":\"\"}", content_type='application/json')

    if not request.POST.get("postId") or request.POST.get("postId").strip() == "":
        return HttpResponse("{\"success\":0, \"error\":\"Invalid post id\", \"userToken\":\"\"}", content_type='application/json')

    if models.Post.objects.filter(id = int(request.POST.get("postId"))).exists():
        post = models.Post.objects.get(id = int(request.POST.get("postId")))

    else:
        return HttpResponse("{\"success\":0, \"error\":\"Post doesnt exist\", \"userToken\":\"\"}", content_type='application/json')

    if models.Tracking.objects.filter(student = student, post = post, status = 1).exists():
        info = models.Tracking.objects.get(student = student, post = post, status = 1)
        info.status = 2
        info.read_on = datetime.datetime.now()
        info.save()

    return HttpResponse("{\"success\":1, \"error\":\"\", \"userToken\":\"\"}", content_type='application/json')


def pushboard_post(request):

    token = request.POST.get('userToken')

    if User.objects.filter(first_name = token).exists():
        student = models.Student.objects.get(user__first_name = token)

    else:
        return HttpResponse("{\"success\":0, \"error\":\"Invalid user token\", \"userToken\":\"\"}", content_type='application/json')

    #Get the classes the student takes part in
    classes_in = student.class_in.all()

    #A query to filter posts
    query = Q()

    #Loop through the sections the student is in to build a query
    for section in classes_in:

        #Add every section the student is in to the query
        query.add( Q( post_to = section.section ), Q.OR )

    posts = models.Post_To_Section.objects.filter( post__id__gt = int(request.POST.get('latestPushboardId'))).filter(query).order_by('-post__id')


    #JSON output
    #Start json array
    output = "{"
    output += "posts: ["

    # Loop through every Post and add them as a json object
    for Post in posts:
        staff = models.Staff.objects.get(user=Post.post.post_by)

        if not models.Tracking.objects.filter(student = student, post = Post.post).exists():
            models.Tracking.objects.create(student = student, post = Post.post, status = 1, del_on = datetime.datetime.now())

        output += "{"
        output += "\"id\":" + str(Post.post.id) + ","
        output += "\"content\":" + "\"" + Post.post.content + "\"" + ","
        output += "\"read\":" + str(models.Tracking.objects.filter(student = student, post = Post.post, status = 2).exists()) + ","

        #Start json array for Post files
        output += "\"files\":" + "["

        for File in Post.post.files.all():
            output += "{"
            output += "\"id\":" + str(File.id) + ","
            output += "\"name\":" + "\"" + File.name + "\"" + ","
            output += "\"extension\":" + "\"" + File.extension + "\"" + ","
            output += "\"size\":" + "\"" + File.file.size + "\"" + ","
            output += "\"uri\":\"/media/" + File.file + "\""
            output += "},"

        if Post.post.files.all().count() > 0:
            # remove the last list separator comma
            output = output[::-1].replace(",", "", 1)[::-1]

        #Close files array
        output += "],"

        #Start json array for Post images
        output += "\"images\":" + "["

        for Image in Post.post.images.all():
            output += "{"
            output += "\"id\":" + str(Image.id) + ","
            output += "\"uri\":\"/media/" + Image.image + "\""
            output += "},"

        if Post.post.images.all().count() > 0:
            # remove the last list separator comma
            output = output[::-1].replace(",", "", 1)[::-1]

        #Close images array
        output += "],"

        output += "\"post_by\":" + "\"" + staff.__str__() + "\"" + ","
        output += "\"post_course\":" + "\"Pushboard\"" + ","
        output += "\"post_courseid\":" + str(-1) + ","
        output += "\"pub_date\":" + "\"" + str(Post.post.pub_date) + "\""
        output += "},"

    # remove the last list separator comma
    output = output[::-1].replace(",", "", 1)[::-1]

    #end of json array
    output += "],"
    output += "\"latestPostId\":" + str(posts[0].id) + ","
    output += "}"

    return HttpResponse(output, content_type='application/json')


def reminders(request):

    token = request.POST.get('userToken')

    if User.objects.filter(first_name = token).exists():
        student = models.Student.objects.get(user__first_name = token)

    else:
        return HttpResponse("{\"success\":0, \"error\":\"Invalid user token\", \"userToken\":\"\"}", content_type='application/json')

    #Get the classes the student takes part in
    classes_in = student.class_in.all()

    #A query to filter posts from Reminder_To_Class
    query = Q()

    #Loop through the classes the student takes to build a query
    for class_in in classes_in:

        #Add every class the student takes to the query
        query.add( Q( reminder_to = class_in.class_in ), Q.OR )

    #Get reminders with ID greater than the specified Reminder_ID
    reminders = models.Reminder_To_Class.objects.filter(query).filter( reminder__id__gt = int(request.POST.get('latestReminderId'))).order_by('-reminder__id')


    #JSON output
    #Start json array
    output = "{"
    output += "reminders: ["

    # Loop through every Course and add them as a json object
    for Reminder in reminders:
        output += "{"
        output += "\"id\":" + str(Reminder.reminder.id) + ","
        output += "\"name\":" + "\"" + Reminder.reminder.title + "\"" + ","
        output += "\"content\":" + "\"" + Reminder.reminder.note + "\"" + ","
        output += "\"submitted\":" + str(models.Assignment_Submission.objects.filter(student = student, assignment = Reminder.reminder).exists()) + ","

        output += "\"reminderType\":" + "\"" + Reminder.reminder.reminder_for + "\"" + ","

        #Start json array for Post files
        output += "\"file\":" + "{"

        for File in Reminder.reminder.file.all():
            output += "\"id\":" + str(File.id) + ","
            output += "\"name\":" + "\"" + File.name + "\"" + ","
            output += "\"extension\":" + "\"" + File.extension + "\"" + ","
            output += "\"size\":" + "\"" + File.file.size + "\"" + ","
            output += "\"uri\":\"/media/" + File.file + "\""

        #Close files array
        output += "},"

        output += "\"due_date\":" + str(Reminder.reminder.due_date) + ","
        output += "\"due_time\":" + str(Reminder.reminder.due_time) + ","
        output += "\"post_by\":" + str(Reminder.reminder.post_by.__str__()) + ","
        output += "\"post_course\":" + str(Reminder.reminder_to.course.name) + ","
        output += "\"post_courseid\":" + str(Reminder.reminder_to.course.id) + ","
        output += "\"pub_date\":" + str(Reminder.reminder.pub_date) + ","
        output += "},"

    # remove the last list separator comma
    output = output[::-1].replace(",", "", 1)[::-1]

    #end of json array
    output += "],"
    output += "\"latestReminderId\":" + str(reminders[0].id) + ","
    output += "}"

    return HttpResponse(output, content_type='application/json')


def course(request):

    token = request.POST.get('userToken')

    if User.objects.filter(first_name = token).exists():
        student = models.Student.objects.get(user__first_name = token)

    else:
        return HttpResponse("{\"success\":0, \"error\":\"Invalid user token\", \"userToken\":\"\"}", content_type='application/json')

    #Get the ids of the courses the student takes
    ids = student.class_in.values_list('course', flat=True)

    #Get all courses taken by a the student[THE 'ID' ATTRIBUTE ISN'T NEEDED FOR THIS REQUEST, ASSIGN ANY VALUE YOU WANT TO 'by-student']
    courses = models.Course.objects.filter(pk__in=set(ids))

    #JSON output
    #Start json array
    output = "["

    # Loop through every Course and add them as a json object
    for Course in courses:
        output += "{"
        output += "\"name\":" + "\"" + Course.name + "\"" + ","
        output += "\"id\":" + str(Course.id)
        output += "},"

    # remove the last list separator comma
    output = output[::-1].replace(",", "", 1)[::-1]

    #end of json array
    output += "]"

    return HttpResponse(output, content_type='application/json')


def forums_user_is_in(request):

    token = request.POST.get('userToken')

    if User.objects.filter(first_name = token).exists():
        student = models.Student.objects.get(user__first_name = token)

    else:
        return HttpResponse("{\"success\":0, \"error\":\"Invalid user token\", \"userToken\":\"\"}", content_type='application/json')

    forums = forum_models.Forum.objects.filter(members = student.user).filter(id__gt = int(request.POST.get('latestForumId'))).order_by('-id')

    #JSON output
    #Start json array
    output = "{"
    output += "reminders: ["

    # Loop through every Forum and add them as a json object
    for forum in forums:
        output += "{"
        output += "\"id\":" + str(forum.id) + ","
        output += "\"name\":" + "\"" + forum.name + "\"" + ","
        output += "\"desc\":" + "\"" + forum.description + "\"" + ","
        output += "\"thumbnail\":" + "\"/media/" + forum.file.file + "\"" + ","

        if student.user.id == forum.creator.id:
            output += "\"creator\":" + str(True)

        else:
            output += "\"creator\":" + str(False)

        output += "},"

    # remove the last list separator comma
    output = output[::-1].replace(",", "", 1)[::-1]

    #end of json array
    output += "],"
    output += "\"latestForumId\":" + str(forums[0].id) + ","
    output += "}"

    return HttpResponse(output, content_type='application/json')

def send_forum_message(request):

    token = request.POST.get('userToken')

    if User.objects.filter(first_name = token).exists():
        student = models.Student.objects.get(user__first_name = token)

    else:
        return HttpResponse("{\"success\":0, \"error\":\"Invalid user token\"}", content_type='application/json')

    if request.POST.get('message').strip() == "":
        return HttpResponse("{\"success\":0, \"error\":\"Message required\"}", content_type='application/json')

    if not forum_models.Forum.objects.get(id = int(request.POST.get('forumId'))).exists():
        return HttpResponse("{\"success\":0, \"error\":\"Forun not found\"}", content_type='application/json')

    content = request.POST.get('message')
    pub_date = datetime.datetime.now()

    post = models.Post.objects.create(content = content, post_type = 6, post_by = student.user, pub_date = pub_date)

    forum = forum_models.Forum.objects.get(id = int(request.POST.get('forumId')))
    forum.posts.add(post)

    return HttpResponse("{\"success\":1, \"error\":\"\"}", content_type='application/json')



def post_action(request):
    token = request.POST.get('userToken')

    if User.objects.filter(first_name = token).exists():
        staff = models.Staff.objects.get(user__first_name = token)

    else:
        return HttpResponse("{\"success\":0, \"error\":\"Invalid user token\"}", content_type='application/json')


        if request.POST.get('action-type') == "chat":
            if not request.POST.get('post-content') or (request.POST.get('post-content').strip() == ""):
                    return HttpResponse("{\"success\":0, \"error\":\"Invalid content\"}", content_type='application/json')

            if request.FILES.get('image-1'):
                if request.FILES['image-1'].name.split('.')[-1].strip().lower() not in ["jpeg","jpg","gif","png","bmp","svg"]:
                    return HttpResponse("{\"success\":0, \"error\":\"Invalid image\"}", content_type='application/json')


            content = request.POST.get('post-content')
            pub_date = datetime.datetime.now()

            post = models.Post.objects.create(content = content, post_type = 4, post_by = staff.user, pub_date = pub_date)

            if request.FILES.get('file-1'):
                name = request.FILES['file-1'].name
                file = models.File.objects.create(file = request.FILES.get('file-1'), name = name, extension = name.split('.')[-1], post_by = staff)
                post.files.add(file)

            if request.FILES.get('image-1'):
                file = models.Image.objects.create(image = request.FILES.get('image-1'), post_by = staff)
                post.images.add(file)

            models.Post_To_Chat.objects.create(post_to = staff.department_in, post = post)

            latest = models.Post_To_Chat.objects.latest('post__pub_date')

            def sizeof_fmt(num, suffix='B'):
                for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
                    if abs(num) < 1024.0:
                        return "%3.1f%s%s" % (num, unit, suffix)
                    num /= 1024.0
                return "%.1f%s%s" % (num, 'Yi', suffix)

            html = ""

            if latest.post.pub_date.day != post.pub_date.day or latest.post.pub_date.month != post.pub_date.month or latest.post.pub_date.year != post.pub_date.year:
                html += "<div class='mx-3 mt-3'>"
                html += "<p>" + post.pub_date.strftime("%B") + " " + post.pub_date.day + "</p>"
                html += "</div>"

            html += "<div class='card card-body push-corners mb-3'>"
            html += "<div class='post-header'>"
            html += "<p class='font-weight-bold'>" + post.post_by.__str__() + "</p></div>"
            html += "<div class='post-images'>"
            for image in post.images.all():
                html += "<div class='mb-3'>"
                html += "<img width='100%' src='/media/" + image.image + "\'/>"
                html += "</div>"
            html += "</div>"
            html += "<div class='post-content'>"
            html += "<p>" + post.content + "</p>"
            html += "</div>"

            html += "<div>"
            for file in post.files.all():
                html += '<div class="file">'
                html += '<div>'
                html += '<a class="link font-weight-bold" href="/media/' + file.file + '">' +  file.name + '['+ file.extension.isupper + ']</a>'
                html += '</div>'
                html += '<div>'
                html += '<p class="meta mb-2">File size:  ' + sizeof_fmt(file.file.size)  + '</p>'
                html += '</div>'
                html += '</div>'
            html += '</div>'

            html += "<div>"
            html += "<div>"
            html += "<span class='meta'>" + str(post.delivered()) + " Views | </span>"
            html += "<span class='meta'>" + post.pub_date.strftime("%b") + ". " + str(post.pub_date.day) + ", " + str(post.pub_date.year) +  ", " + post.pub_date.strftime("%I") + ":" + post.pub_date.strftime("%M") + " "

            if post.pub_date.strftime("%p") == "AM":
                html += "a.m"

            else:
                html += "p.m"

            html += "</span>"
            html += "</div>"
            html += "</div>"
            html += "</div>"

            return HttpResponse("{\"success\":1, \"error\":\"\"}", content_type='application/json')


        if (request.POST.get('post-content').strip() == ""):
                return HttpResponse("{\"success\":0, \"error\":\"Invalid content\"}", content_type='application/json')

        if not request.POST.getlist('section-recipients'):
            if not request.POST.getlist('class-recipients'):
                return HttpResponse("{\"success\":0, \"error\":\"No recipient\"}", content_type='application/json')

        if request.FILES.get('file-1'):
            if request.POST.get('file-name-1').strip() == "":
                return HttpResponse("{\"success\":0, \"error\":\"Invalid file-1\"}", content_type='application/json')

        if request.FILES.get('file-2'):
            if request.POST.get('file-name-2').strip() == "":
                return HttpResponse("{\"success\":0, \"error\":\"Invalid file-2\"}", content_type='application/json')

        if request.FILES.get('file-3'):
            if request.POST.get('file-name-3').strip() == "":
                return HttpResponse("{\"success\":0, \"error\":\"Invalid file-3\"}", content_type='application/json')

        if request.FILES.get('image-1'):
            if request.FILES['image-1'].name.split('.')[-1].strip().lower() not in ["jpeg","jpg","gif","png","bmp","svg"]:
                return HttpResponse("{\"success\":0, \"error\":\"Invalid image-\"}", content_type='application/json')

        if request.FILES.get('image-2'):
                if request.FILES['image-2'].name.split('.')[-1].strip().lower() not in ["jpeg","jpg","gif","png","bmp","svg"]:
                    return HttpResponse("{\"success\":0, \"error\":\"Invalid image-2\"}", content_type='application/json')

        content = request.POST.get('post-content')
        pub_date = datetime.datetime.now()

        if len(request.POST.getlist('section-recipients')) > 0:
            post = models.Post.objects.create(content = content, post_type = 1, post_by = staff, pub_date = pub_date)

            if request.FILES.get('file-1'):
                    name = request.POST.get('file-name-1')
                    file = models.File.objects.create(file = request.FILES.get('file-1'), name = name, extension = request.FILES['file-1'].name.split('.')[-1], post_by = staff)
                    post.files.add(file)

            if request.FILES.get('file-2'):
                    name = request.POST.get('file-name-2')
                    file = models.File.objects.create(file = request.FILES.get('file-2'), name = name, extension = request.FILES['file-1'].name.split('.')[-1], post_by = staff)
                    post.files.add(file)

            if request.FILES.get('file-3'):
                    name = request.POST.get('file-name-3')
                    file = models.File.objects.create(file = request.FILES.get('file-3'), name = name, extension = request.FILES['file-1'].name.split('.')[-1], post_by = staff)
                    post.files.add(file)


            if request.FILES.get('image-1'):
                file = models.Image.objects.create(image = request.FILES['image-1'], post_by = staff)
                post.images.add(file)

            if request.FILES.get('image-2'):
                file = models.Image.objects.create(image = request.FILES['image-2'], post_by = staff)
                post.images.add(file)



            section_recipients = request.POST.getlist('section-recipients')

            for recipient in section_recipients:
                detail = recipient.split('-')

                if detail[0] == 'year':
                    for section in models.Section.objects.filter(department_in__id = int(detail[1]), year = int(detail[2])):
                        models.Post_To_Section.objects.create(post_to = section, post = post)

                elif detail[0] == 'section':
                    section = models.Section.objects.get(id = int(detail[1]))
                    models.Post_To_Section.objects.create(post_to = section, post = post)


        if len(request.POST.getlist('class-recipients')) > 0:
            post = models.Post.objects.create(content = content, post_type = 2, post_by = staff.user, pub_date = pub_date)

            if request.FILES.get('file-1'):
                    name = request.POST.get('file-name-1')
                    file = models.File.objects.create(file = request.FILES.get('file-1'), name = name, extension = request.FILES['file-1'].name.split('.')[-1], post_by = staff)
                    post.files.add(file)

            if request.FILES.get('file-2'):
                    name = request.POST.get('file-name-2')
                    file = models.File.objects.create(file = request.FILES.get('file-2'), name = name, extension = request.FILES['file-1'].name.split('.')[-1], post_by = staff)
                    post.files.add(file)

            if request.FILES.get('file-3'):
                    name = request.POST.get('file-name-3')
                    file = models.File.objects.create(file = request.FILES.get('file-3'), name = name, extension = request.FILES['file-1'].name.split('.')[-1], post_by = staff)
                    post.files.add(file)


            if request.FILES.get('image-1'):
                file = models.Image.objects.create(image = request.FILES['image-1'], post_by = staff)
                post.images.add(file)

            if request.FILES.get('image-2'):
                file = models.Image.objects.create(image = request.FILES['image-2'], post_by = staff)
                post.images.add(file)

            class_recipients = request.POST.getlist('class-recipients')

            for recipient in class_recipients:
                detail = recipient.split('-')

                class_ = models.Instructor_Teaches.objects.get(section__id = int(detail[0]), course__id = int(detail[1]))

                models.Post_To_Class.objects.create(post_to = class_, post = post)


        return HttpResponse("{\"success\":0, \"error\":\"Invalid content\"}", content_type='application/json')



def class_list(request):

    token = request.POST.get('userToken')

    if User.objects.filter(first_name = token).exists():
        staff = models.Staff.objects.get(user__first_name = token)

    else:
        return HttpResponse("{\"success\":0, \"error\":\"Invalid user token\"}", content_type='application/json')

    #Check if the api request is based on a specific Educational Institution
    if request.GET.get('by-department'):

        #Get all sections in that specific Educational Institution(THE 'ID' ATTRIBUTE SHOULD BE SENT/USED TO SPECIFY THE INSTANCE)
        classes = models.Instructor_Teaches.objects.filter(section__department_in__id = int(request.GET.get('by-department')))

    #Check if the api request is based on a specific Department
    elif request.GET.get('by-student'):
        if models.Student.objects.filter(user=request.user).exists():
            #Get all sections in that specific Department(THE 'ID' ATTRIBUTE SHOULD BE SENT/USED TO SPECIFY THE INSTANCE)
            classes = models.Student.objects.get(user=request.user).class_in.all()

        else:
            return HttpResponse("{\"success\":0, \"error\":\"Invalid user-type\"}", content_type='application/json')
    else:
        classes =  models.Instructor_Teaches.objects.filter(instructor__user = staff.user).order_by('section__department_in','section__year','section__section_id')

    #JSON output
    #Start json array
    output = "["

    # Loop through every Section and add them as a json object

    for classs in classes:
        output += "{"

        output += "\"section\":"
        output += "{"

        output += "\"id\":" + str(classs.section.id) + ","
        output += "\"department\":" + "\"" + classs.section.department_in.name + "\"" + ","
        output += "\"year\":" + str(classs.section.year) + ","
        output += "\"section_id\":" + "\"" + classs.section.section_id + "\""

        output += "},"

        output += "\"course\":"
        output += "{"

        output += "\"id\":" + str(classs.course.id) + ","
        output += "\"name\":" + "\"" + classs.course.name + "\""

        output += "}"

        output += "},"

    # remove the last list separator comma
    output = output[::-1].replace(",", "", 1)[::-1]

    #end of json array
    output += "]"

    return HttpResponse(output, content_type='application/json')
