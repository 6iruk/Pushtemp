from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from main.models import *
from push_page.models import *
from main.forms import Lecturerform
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.core import serializers
import datetime, zipfile, io

def index(request):
        daily = timezone.now().day
        quote = Quote.objects.get(id=1)
        studyfield = StudyField.objects.get(code='CoSc')
        sections = studyfield.section_set.order_by('year')
        context = {'quote':quote,'sections':sections}
        return render(request, 'main/index.html',context)

def section(request,section_code):
        section = Section.objects.get(code=section_code)
        courses = section.course.order_by('name')
        material_count = []
        for course in courses:
                material_count.append(course.get_material_count(section))
        quote = Quote.objects.get(id=1)
        now = datetime.datetime.now()
        announcements = section.announcement_set.order_by('-pub_date').filter(exp_date__gt = now)
        for announcement in announcements:
                announcement.inc_count()
        this_week = []
        a_week_ago = now - datetime.timedelta(days=7)
        this_week = section.material_set.order_by('-pub_date').filter(pub_date__range=(a_week_ago , now))
        context = {'section':section,'courses':courses, 'quote':quote, 'announcements':announcements, 'this_week':this_week}
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
                        newzip.write("%s"%material.file.name, material.name + '.%s'%material.ext())
                newzip.close()
                response = HttpResponse(strio.getvalue(), content_type='application/x-zip-compressed')
                response['Content-Disposition'] = 'attachment; filename="Push-%s.zip"'%course_name
                return response             
        else:
                section = Section.objects.get(code=section_code)
                courses = section.course.order_by('name')
                course = Course.objects.get(name=course_name.replace('_', ' '))
                materials = course.material_set.order_by('-pub_date').filter(section=section)
                quote = Quote.objects.get(id=1)
                context = {'section':section, 'course':course, 'courses':courses, 'materials':materials, 'quote':quote}
                return render(request,'main/course_view.html',context)

def file_request(request, material_id):
        material = get_object_or_404(Material, id=material_id)
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
                quote = Quote.objects.get(id=1)
                return render(request, 'main/login.html',{'quote':quote})
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
                if user.is_active:
                        login(request,user)
                        return redirect('portal')
                else:
                        message = 'Your user account is not active.'
                        quote = Quote.objects.get(id=1)
                        return render(request, 'main/login.html', {'message':message, 'quote':quote})
        else:
                message = 'You have entered invalid username or password. Contact Addis - 0913350082 for help.'
                quote = Quote.objects.get(id=1)
                return render(request, 'main/login.html', {'message':message, 'quote':quote})
        
def portal(request):
        success = False
        if (request.method == 'POST'):
                if(request.POST['request_type'] == 'Logout'):
                        logout(request)
                        return redirect('Home')
                
                if(request.POST['request_type'] == 'announcement'):
                        message = request.POST.get('message')
                        if request.POST.get('ann_type') == 'section':
                                section = [Section.objects.get(code=x) for x in request.POST.getlist('section')]
                        elif request.POST.get('ann_type') == 'course':
                                section = [Section.objects.filter(course__name=x) for x in request.POST.getlist('course')]
                        lecturer = Lecturer.objects.get(user=request.user)
                        is_urgent = bool(request.POST.get('urgent'))
                        pub_date = datetime.datetime.now()
                        exp_date = pub_date + datetime.timedelta(days=int(request.POST.get('duration')))
                        if request.FILES.get('file'):
                                file1 = request.FILES.get('file')
                                if request.FILES.get('file_'):
                                        file2 = request.FILES.get('file_')  
                                        ann =  Announcement(lecturer=lecturer, message=message, is_urgent=is_urgent, file1=file1, file2=file2, pub_date=pub_date, exp_date=exp_date,count=0)  
                                else:
                                        ann =  Announcement(lecturer=lecturer, message=message, is_urgent=is_urgent, file1=file1, pub_date=pub_date, exp_date=exp_date,count=0)
                        elif request.FILES.get('file_'):
                                file1 = request.FILES.get('file_')
                                ann =  Announcement(lecturer=lecturer, message=message, is_urgent=is_urgent, file1=file1, pub_date=pub_date, exp_date=exp_date,count=0)
                        else:
                                ann =  Announcement(lecturer=lecturer, message=message, is_urgent=is_urgent, pub_date=pub_date, exp_date=exp_date,count=0)
                        ann.save()
                        if request.POST.get('ann_type') == 'section':
                                for sec in section:
                                        ann.section.add(sec)
                        if request.POST.get('ann_type') == 'course':
                                for sec in section:
                                        for s in sec:
                                                ann.section.add(s)
                        ann.save()                
                        success = True
                        
                if (request.POST['request_type'] =='material'):
                        name = request.POST.get('name')
                        description = request.POST.get('description')   
                        file = request.FILES.get('file_data')
                        pub_date = datetime.datetime.now()
                        lecturer = Lecturer.objects.get(user=request.user)
                        course = Course.objects.get(id=request.POST.get('course'))
                        material = Material(name=name,description=description,file=file,pub_date=pub_date,lecturer=lecturer,course=course,count=0)
                        material.save() 
                        if request.POST.get('mat_type') == 'all':
                                sections = Section.objects.filter(course=course).distinct()
                        elif request.POST.get('mat_type') == 'my':
                                sections = set(Section.objects.filter(course=course)).intersection(lecturer.section.all()).distinct
                        elif request.POST.get('mat_type') == 'section':
                                sections = [Section.objects.get(code=x)for x in request.POST.getlist('mat_section')]

                        for section in sections:
                                material.section.add(section)
                        material.save()
                        success = True

        if request.user.is_authenticated():
                user = request.user
                if not Lecturer.objects.filter(user=user).exists():
                         return redirect('first_login')
                lecturer = get_object_or_404(Lecturer, user=user)   
                course = Course.objects.filter(lecturer=lecturer)
                sections = lecturer.section.get_queryset()
                quote = Quote.objects.get(id=1)
                prev = Announcement.objects.filter(lecturer=lecturer).order_by('-pub_date')
                context = {'quote':quote,'lecturer':lecturer, 'course':course, 'sections':sections, 'prev':prev, 'success':success}    
                return render(request, 'main/portal.html', context) 
        else:
                return redirect('login')
  
def first_login(request):
        if (not(request.user.is_authenticated()) or Lecturer.objects.filter(user=request.user).exists()):
                return HttpResponse('<h1>PAGE NOT FOUND!!!</h1>')
        if request.method == 'POST':
                form = Lecturerform(request.POST)
                #form =request.user
                if not form.is_valid():
                        context = {'form':form}
                        return render(request,'main/first_login.html',context)
                form.save()
                user = User.objects.get(username=request.user)
                user.set_password(request.POST['new_password'])
                user.username = request.POST['lect_id'].lower()
                user.save()
                return redirect('login')
        else:
                form = Lecturerform(initial={'user':request.user})
                context = {'form':form,'user':request.user}
                return render(request,'main/first_login.html',context)
