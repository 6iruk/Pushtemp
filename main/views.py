from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from itertools import chain
from operator import attrgetter
from main.models import *
from push_page.models import *
from main.forms import Lecturerform
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.core import serializers
import datetime, zipfile, io
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def index(request):
        sections = Section.objects.filter(department__code='AAU4k-CoSc').order_by('year','number')

        context = {'sections':sections}
        return render(request, 'main/index.html',context)

def section(request,section_code):
        section = Section.objects.get(code=section_code)
        section_takes = section.take.order_by('name')
        now = datetime.datetime.now()
        announcements = Announcement_To.objects.filter(to__section = section, announcement__exp_date__gt = now).order_by('-announcement__pub_date')
        for announcement in announcements:
                announcement.announcement.inc_count()
        this_week = []
        a_week_ago = now - datetime.timedelta(days=7)
        uploads_this_week = Material_To.objects.filter(to__section = section, material__pub_date__range=(a_week_ago , now)).order_by('-material__pub_date')

        context = {'section':section,'courses':section_takes, 'announcements':announcements, 'this_week':uploads_this_week}
        return render(request,'main/section.html',context)

def course_view(request,section_code,course_name):
        if(request.method == "POST"):
                matter = []
                formset = request.POST.copy()
                formset.pop('csrfmiddlewaretoken')
                for material in formset:
                        matter.append(Material.objects.get(id=material))
                strio = io.BytesIO()    
                newzip = zipfile.ZipFile(strio,'a')
                for material in matter:
                        newzip.write(os.path.join(BASE_DIR, "uploads/%s"%material.file.name), material.name + '.%s'%material.ext())
                        material.inc_count()
                newzip.close()
                response = HttpResponse(strio.getvalue(), content_type='application/x-zip-compressed')
                response['Content-Disposition'] = 'attachment; filename="Push-%s.zip"'%course_name
                return response             
        else:
                section = Section.objects.get(code=section_code)
                section_takes = section.take.order_by('name')
                course = Course.objects.get(name=course_name.replace('_', ' '))
                materials_for_course = Material_To.objects.filter(to__section = section, to__course = course).order_by('-material__pub_date')

                context = {'section':section, 'course':course, 'courses':section_takes, 'materials':materials_for_course}
                return render(request,'main/course_view.html',context)

def file_request(request, material_id):
        material = get_object_or_404(Material, id=material_id)
        material.inc_count()
        ext = material.file.name.split('.')[-1]
        response = HttpResponse(content_type='application/%s'%ext)
        file_name = material.name + '.' + ext
        response['Content-Disposition'] = 'attachment; filename="%s"'%file_name
        response.write(material.file.read())
        return response

def login_view(request):
        if not request.POST:
                if request.user.is_authenticated():
                   return redirect('portal')

                return render(request, 'main/login.html')
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
                if user.is_active:
                        login(request,user)
                        return redirect('portal')
                else:
                        message = 'Your user account is not active.'
                        return render(request, 'main/login.html', {'message':message})
        else:
                message = 'You have entered invalid username or password. Contact Addis - 0913350082 for help.'
                return render(request, 'main/login.html', {'message':message})
        
def portal(request):
        success = False
        if (request.method == 'POST'):
                if(request.POST['request_type'] == 'Logout'):
                        logout(request)
                        return redirect('Home')
                
                if(request.POST['request_type'] == 'announcement'):
                        message = request.POST.get('message')
                        pub_date = datetime.datetime.now()
                        exp_date = pub_date + datetime.timedelta(days=int(request.POST.get('duration')))
                        ann =  Announcement(pub_date = pub_date, exp_date = exp_date, message = message, count = 0)
                        ann.save()

                        for section in request.POST.getlist('sections'):
                                to = Announcement_To(to = Teacher_Teaches.objects.get(section__id = int(section), teacher__user = request.user), announcement = ann, pub_date = pub_date)
                                to.save()                        
                        success = True
                        
                if (request.POST['request_type'] == 'material'):
                        name = request.POST.get('name')
                        description = request.POST.get('description')   
                        file = request.FILES.get('file_data')
                        pub_date = datetime.datetime.now()
                        material = Material(name = name, description = description, file = file, pub_date = pub_date, teacher = Teacher.objects.get(user=request.user), count = 0)
                        material.save()
                        
                        for section in request.POST.getlist('mat_sections'):
                                to = Material_To(to = Teacher_Teaches.objects.get(section_id = int(section), teacher__user = request.user), material = material, pub_date = pub_date)
                                to.save() 
                        success = True

        if request.user.is_authenticated():
                user = request.user
                if not Teacher.objects.filter(user=user).exists():
                         return redirect('first_login')
                teacher = get_object_or_404(Teacher, user=user)
                teachs = Teacher_Teaches.objects.filter(teacher = teacher)
                prev = sorted(chain(Announcement_To.objects.filter(to__teacher = teacher),Material_To.objects.filter(to__teacher = teacher)),key=attrgetter('pub_date'))

                context = {'lecturer':teacher, 'sections':teachs, 'prev':prev, 'success':success}    
                return render(request, 'main/portal.html', context) 
        else:
                return redirect('login')
  
def first_login(request):
        if (not(request.user.is_authenticated()) or Teacher.objects.filter(user=request.user).exists()):
                if(request.GET.get('username','') != '' and request.GET.get('password','') != ''):
                        username = request.GET['username']
                        password = request.GET['password']
                        user = authenticate(username=username, password=password)
                        if user is not None:
                                if user.is_active:
                                        login(request,user)
                                        return redirect('portal')                        
                return HttpResponse('<h1>PAGE NOT FOUND!!!</h1>')
        if request.method == 'POST':
                teacher = Teacher(title = request.POST['title'], user = request.user, first_name = request.POST['first_name'], last_name = request.POST['last_name'], staffid = request.POST['staffid'], department = Department.objects.get(id=int(request.POST['department'])))
                teacher.save()
                
                for pair in request.POST.getlist('section-course'):
                        pair_arr = pair.split('-')
                        teaches = Teacher_Teaches(teacher = teacher, section = Section.objects.get(id = int(pair_arr[0])), course = Course.objects.get(id = int(pair_arr[1])))
                        teaches.save()

                user = User.objects.get(username=request.user)
                user.username = request.POST['staffid']
                user.set_password(request.POST['new_password'])
                user.save()
                
                return redirect('login')
        else:
                departments = Department.objects.all()
                sections = Section.objects.all()
                
                context = {'user':request.user,'departments':departments, 'sections':sections}
                return render(request,'main/first_login.html',context)
