from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from itertools import chain
from operator import attrgetter
from django.db.models import Q, Max, Count
from main.models import *
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.core import serializers
import datetime, zipfile, io
import os
import random
from openpyxl import load_workbook
import requests

##import sendgrid
##from sendgrid.helpers.mail import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def index(request):
    departments = Department.objects.all()

    context = {'departments':departments}
    return render(request, 'main/index.html', context)



def students_signup_page(request):
    if(request.method == "POST"):
        form = request.POST.copy()
        error = [False,False,False,False,False, False]
        departments = Department.objects.all()

        if not request.POST.get('first_name') or (request.POST.get('first_name').strip() == ""):
            error[0] = True

        if not request.POST.get('last_name') or (request.POST.get('last_name').strip() == ""):
            error[1] = True

        if request.POST.get('email') and request.POST.get('email').strip() != "":
            e = request.POST.get('email')
            if (e.strip().rfind('.') == -1 or e.strip().rfind('@') == -1 or (e.strip().rfind('.') <= e.strip().rfind('@'))):
                error[2] = True

        if not request.POST.get('department') or not Department.objects.filter(id = int(request.POST.get('department'))).exists():
            error[3] = True

        else:
            department = Department.objects.get(id = int(form['department']))

        if not request.POST.get('reg_id') or (request.POST.get('reg_id').strip() == ""):
            error[4] = True

        if len(request.POST.get('reg_id').split('/')) != 3 or request.POST.get('reg_id').split('/')[0].upper() != "NSR" or not request.POST.get('reg_id').split('/')[1].isdigit() or not request.POST.get('reg_id').split('/')[2].isdigit():
            error[4] = True

        if User.objects.filter(username = request.POST.get('reg_id').replace("/","-")).exists():
            error[5] = True

        if error[0] or error[1] or error[2] or error[3] or error[4] or error[5]:
            return render(request, 'main/student/students-signup.html', {'form': form, 'error':error, 'departments':departments})

        max_year = department.section_set.all().aggregate(Max('year'))
        year_html = ""

        for x in range(max_year['year__max']):
            year_html += "<option value=" + str(department.id) + "-" + str(x + 1) + ">Year " + str(x + 1) + "</option>"

        context = {'form' : form, 'year_html' : year_html, 'departments':departments}
        return render(request, 'main/student/students-signup2.html', context)

    departments = Department.objects.all()

    context = {'departments':departments}
    return render(request, 'main/student/students-signup.html', context)



def login_page(request):
    if request.user.is_authenticated:
        logout(request)

    return render(request, 'main/login.html')



def student_account_page(request):
    if request.user.is_authenticated and Student.objects.filter(user=request.user).exists():
        student = Student.objects.get(user=request.user)

    else:
         return HttpResponse('<h1>PAGE NOT FOUND!!!</h1>')

    classes_in = student.class_in.all()
    query = Q()
    for class_in in classes_in:

        #Add every class the student takes to the query
        query.add( Q( post_to = class_in ), Q.OR )

    query2 = Q()
    for section in classes_in:

        #Add every section the student is in to the query
        query2.add( Q( post_to = section.section ), Q.OR )


    read_tracker = []
    wall = []
    pushboard = []
    
    if not classes_in.count() == 0:
        wall = list(Post_To_Class.objects.filter(query).order_by('-post__pub_date'))
        pushboard = Post_To_Section.objects.filter(query2).order_by('-post__pub_date')
    
    for post in wall:
        if not Tracking.objects.filter(student = student, post = post.post).exists():
            Tracking.objects.create(student = student, post = post.post, status = 1, del_on = datetime.datetime.now())

        if not Tracking.objects.filter(student = student, post = post.post, status = 2).exists():
            read_tracker.append(post.id)

    for post in pushboard:
        if not Tracking.objects.filter(student = student, post = post.post).exists():
            Tracking.objects.create(student = student, post = post.post, status = 1, del_on = datetime.datetime.now())

    reminder = Reminder_To_Class.objects.all()

    sections = student.department_in.section_set.all().order_by('department_in','year','section_id')

    departments = Department.objects.all()

    context = {'wall':wall, 'sections':sections, 'reminder':reminder, 'student':student, 'departments':departments,'read_tracker':read_tracker}
    return render(request, 'main/student/student-account.html', context)



def staff_account_page(request):
    if request.user.is_authenticated and Staff.objects.filter(user=request.user).exists():
        staff = Staff.objects.get(user=request.user)

    else:
         return HttpResponse('<h1>PAGE NOT FOUND!!!</h1>')

    posts_to_class = Post_To_Class.objects.filter(post__post_by = staff).order_by('-post__pub_date')
    posts_to_section = Post_To_Section.objects.filter(post__post_by = staff).order_by('-post__pub_date')
    posts = sorted((list(posts_to_section) + list(posts_to_class)), key=lambda x: x.post.pub_date)

    group_posts = Post_To_Chat.objects.filter(post_to = staff.department_in)

    classes = Instructor_Teaches.objects.filter(instructor=staff)

    x = Q()
    for course in staff.department_in.course_set.all():
        x = x | Q(section_takes = course)
    sections = Section.objects.filter(x).distinct().order_by('department_in','year','section_id')

    department_sections = staff.department_in.section_set.all().order_by('department_in','year','section_id')
    departments = Department.objects.all()

    if classes.count() < 1:
        is_first = True

    else:
        is_first = False
    context = {'departments':departments, 'posts':posts, 'staff':staff, 'is_first':is_first, 'classes':classes, 'sections':sections,'department_sections':department_sections, 'titles':(('Mr.','Mr.'),('Ms.','Ms.'),('Mrs.','Mrs.'),('Dr.','Doctor'),('Prof.','Professor'))}
    return render(request, 'main/staff/staff-account.html', context)



def forum_home(request):


    return render(request, 'main/forum/forum_home.html')



def forum_create(request):

    return render(request, 'main/forum/forum_create.html', context)



def forum_feed(request):

    return render(request, 'main/forum/forum_feed.html', context)



def forum_search(request):

    return render(request, 'main/forum/forum_search.html', context)



def teacher_xls_page(request):
    if request.method == 'POST':
        wb = load_workbook(filename=request.FILES['xlsx'])
        sheet = wb.active

        rows = sheet.rows
        sent = []
        not_sent = []
        exists = []
        code = []
        for row in rows:
            for cell in row:
                email = cell.value

                if email:
                    password = "aau" + str(random.randint(10000,99999))

                    if not User.objects.filter(username = email).exists():
                        user = User(username = email, email = "staff@aau.com")
                        user.set_password(password)
                        cnf = open(os.path.join(BASE_DIR, 'mailgin_api.cnf'), "r")
                        key = cnf.readline().strip()

                        template1 = open(os.path.join(BASE_DIR, 'email_template1.html'), "r")
                        html = template1.read()
                        html += email+ "<br>Password: " + password

                        template2 = open(os.path.join(BASE_DIR, 'email_template2.html'), "r")
                        html += template2.read()

                        response = requests.post("https://api.mailgun.net/v3/aaupush.com/messages", auth=("api", key), data={"from": "AAU PUSH <aaupush@gmail.com>", "to": email, "subject": "AAU Push Account Activation", "html": html})

                        code.append(response.text)
                        if response.status_code != 200:
                            not_sent.append(email)

                        else:
                            user.save()
                            sent.append(email)

                    else:
                        exists.append(email)
        return render(request, 'main/staff/teacher-xls.html', {'not_sent':not_sent, 'sent':sent, 'exists':exists, 'code':code})

    return render(request, 'main/staff/teacher-xls.html')



def first_login(request):
       if request.method == 'POST':
               if request.user.is_authenticated and not Staff.objects.filter(user=request.user).exists() and not Student.objects.filter(user=request.user).exists() and request.user.email == "staff@aau.com":
                   department = Department.objects.get(id=int(request.POST['department']))
                   teacher = Staff(title = request.POST['title'], user = request.user, first_name = request.POST['first-name'], last_name = request.POST['last-name'], email = request.POST['email'], university_in = department.university_in , department_in = department, role = "Instructor")
                   teacher.save()

                   user = request.user
                   user.set_password(request.POST['new_password'])
                   user.username = request.POST['email']
                   user.save()

                   return redirect('Log In')
               else:
                   return HttpResponse('<h1>PAGE NOT FOUND!!!</h1>')
       else:
               if request.user.is_authenticated and not Staff.objects.filter(user=request.user).exists() and not Student.objects.filter(user=request.user).exists() and request.user.email == "staff@aau.com":
                   departments = Department.objects.all()

                   context = {'user':request.user,'departments':departments}
                   return render(request,'main/staff/first_login.html',context)
               else:
                   return HttpResponse('<h1>PAGE NOT FOUND!!!</h1>')



def feedback_page(request):

    return render(request, 'main/feedback.html')


##def section(request,section_code):
##        section = Section.objects.get(code=section_code)
##        section_takes = section.take.order_by('name')
##        now = datetime.datetime.now()
##        announcements = Announcement_To.objects.filter(to__section = section, announcement__exp_date__gt = now).order_by('-announcement__pub_date')
##        for announcement in announcements:
##                announcement.announcement.inc_count()
##        this_week = []
##        a_week_ago = now - datetime.timedelta(days=7)
##        uploads_this_week = Material_To.objects.filter(to__section = section, material__pub_date__range=(a_week_ago , now)).order_by('-material__pub_date')
##
##        context = {'section':section,'courses':section_takes, 'announcements':announcements, 'this_week':uploads_this_week}
##        return render(request,'main/section.html',context)
##
##def course_view(request,section_code,course_name):
##        if(request.method == "POST"):
##                matter = []
##                formset = request.POST.copy()
##                formset.pop('csrfmiddlewaretoken')
##                for material in formset:
##                        matter.append(Material.objects.get(id=material))
##                strio = io.BytesIO()
##                newzip = zipfile.ZipFile(strio,'a')
##                for material in matter:
##                        newzip.write(os.path.join(BASE_DIR, "uploads/%s"%material.file.name), material.name + '.%s'%material.ext())
##                        material.inc_count()
##                newzip.close()
##                response = HttpResponse(strio.getvalue(), content_type='application/x-zip-compressed')
##                response['Content-Disposition'] = 'attachment; filename="Push-%s.zip"'%course_name
##                return response
##        else:
##                section = Section.objects.get(code=section_code)
##                section_takes = section.take.order_by('name')
##                course = Course.objects.get(name=course_name.replace('_', ' '))
##                materials_for_course = Material_To.objects.filter(to__section = section, to__course = course).order_by('-material__pub_date')
##
##                context = {'section':section, 'course':course, 'courses':section_takes, 'materials':materials_for_course}
##                return render(request,'main/course_view.html',context)
##
##def file_request(request, material_id):
##        material = get_object_or_404(Material, id=material_id)
##        material.inc_count()
##        ext = material.file.name.split('.')[-1]
##        response = HttpResponse(content_type='application/%s'%ext)
##        file_name = material.name + '.' + ext
##        response['Content-Disposition'] = 'attachment; filename="%s"'%file_name
##        response.write(material.file.read())
##        return response
##
##def login_view(request):
##        if not request.POST:
##                if request.user.is_authenticated():
##                   return redirect('portal')
##
##                return render(request, 'main/login.html')
##        username = request.POST.get('username')
##        password = request.POST.get('password')
##        user = authenticate(username=username, password=password)
##        if user is not None:
##                if user.is_active:
##                        login(request,user)
##                        return redirect('portal')
##                else:
##                        message = 'Your user account is not active.'
##                        return render(request, 'main/login.html', {'message':message})
##        else:
##                message = 'You have entered invalid username or password. Contact Addis - 0913350082 for help.'
##                return render(request, 'main/login.html', {'message':message})
##
##def portal(request):
##        success = False
##        if (request.method == 'POST'):
##                if(request.POST['request_type'] == 'Logout'):
##                        logout(request)
##                        return redirect('Home')
##
##                if(request.POST['request_type'] == 'announcement'):
##                        message = request.POST.get('message')
##                        pub_date = datetime.datetime.now()
##                        exp_date = pub_date + datetime.timedelta(days=int(request.POST.get('duration')))
##                        ann =  Announcement(pub_date = pub_date, exp_date = exp_date, message = message, count = 0)
##                        ann.save()
##
##                        for section in request.POST.getlist('sections'):
##                                to = Announcement_To(to = Teacher_Teaches.objects.get(section__id = int(section), teacher__user = request.user), announcement = ann, pub_date = pub_date)
##                                to.save()
##                        success = True
##
##                if (request.POST['request_type'] == 'material'):
##                        name = request.POST.get('name')
##                        description = request.POST.get('description')
##                        file = request.FILES.get('file_data')
##                        pub_date = datetime.datetime.now()
##                        material = Material(name = name, description = description, file = file, pub_date = pub_date, teacher = Teacher.objects.get(user=request.user), count = 0)
##                        material.save()
##
##                        for section in request.POST.getlist('mat_sections'):
##                                to = Material_To(to = Teacher_Teaches.objects.get(section_id = int(section), teacher__user = request.user), material = material, pub_date = pub_date)
##                                to.save()
##                        success = True
##
##        if request.user.is_authenticated():
##                user = request.user
##                if not Teacher.objects.filter(user=user).exists():
##                         return redirect('first_login')
##                teacher = get_object_or_404(Teacher, user=user)
##                teachs = Teacher_Teaches.objects.filter(teacher = teacher)
##                prev = sorted(chain(Announcement_To.objects.filter(to__teacher = teacher),Material_To.objects.filter(to__teacher = teacher)),key=attrgetter('pub_date'))
##
##                context = {'lecturer':teacher, 'sections':teachs, 'prev':prev, 'success':success}
##                return render(request, 'main/portal.html', context)
##        else:
##                return redirect('login')
##
##def first_login(request):
##        if (not(request.user.is_authenticated()) or Teacher.objects.filter(user=request.user).exists()):
##                if(request.GET.get('username','') != '' and request.GET.get('password','') != ''):
##                        username = request.GET['username']
##                        password = request.GET['password']
##                        user = authenticate(username=username, password=password)
##                        if user is not None:
##                                if user.is_active:
##                                        login(request,user)
##                                        return redirect('portal')
##                return HttpResponse('<h1>PAGE NOT FOUND!!!</h1>')
##        if request.method == 'POST':
##                teacher = Teacher(title = request.POST['title'], user = request.user, first_name = request.POST['first_name'], last_name = request.POST['last_name'], staff_id = request.POST['staffid'], email = request.POST['email'], department = Department.objects.get(id=int(request.POST['department'])))
##                teacher.save()
##
##                for pair in request.POST.getlist('section-course'):
##                        pair_arr = pair.split('-')
##                        teaches = Teacher_Teaches(teacher = teacher, section = Section.objects.get(id = int(pair_arr[0])), course = Course.objects.get(id = int(pair_arr[1])))
##                        teaches.save()
##
##                user = User.objects.get(username=request.user)
##                user.username = request.POST['staffid']
##                user.set_password(request.POST['new_password'])
##                user.save()
##
##                return redirect('login')
##        else:
##                departments = Department.objects.all()
##                sections = Section.objects.all().order_by('year')
##
##                context = {'user':request.user,'departments':departments, 'sections':sections}
##                return render(request,'main/first_login.html',context)
##def forgot_password(request):
##        return render(request,'main/forgot_password.html')
