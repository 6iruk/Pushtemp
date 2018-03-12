from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.db.models import Q
from main.models import User
from main.models import University
from main.models import Department
from main.models import Course
from main.models import Section
from main.models import Teacher
from main.models import Teacher_Teaches
from main.models import Announcement
from main.models import Material
from main.models import Announcement_To
from main.models import Material_To

# Create your views here.
def index(request):
        return HttpResponse("Welcome to aau push APIs.")

def courses(request):
        if request.GET.get('sections') and request.GET.get('department'):
                section_codes = request.GET.get('sections').split('-')
                courses_list = [Section.objects.get(id=int(x)).take.all().filter(department__id = int(request.GET.get('department'))) for x in section_codes]
                courses = [y for x in courses_list for y in x]                
                
        elif request.GET.get('sections'):
                section_codes = request.GET.get('sections').split('-')
                courses_list = [Section.objects.get(id=int(x)).take.all() for x in section_codes]
                courses = [y for x in courses_list for y in x]

        elif request.GET.get('department'):
                courses = Course.objects.filter(department__id=int(request.GET.get('department')))

        else :
                return HttpResponse("Incorrect API request format. Refer to the docmumentaion.")
        
        #JSON output
        #Start json array
        output = "[";

        # Loop through every study field and add them as a json object
        for course in courses:
                output += "{"
                output += "\"id\":" + str(course.id) + ","
                output += "\"name\":" + "\"" + course.name + "\"" + ","
                output += "\"department\":" + "\"" + course.department.name + "\"" + ","
                output += "\"code\":" + "\"" + course.code + "\"" + ","
                output += "\"course_code\":" + "\"" + course.course_code + "\""
                output += "},"

        # remove the last list separator comma
        output = output[::-1].replace(",", "", 1)[::-1]

        #end of json array
        output += "]"

        return HttpResponse(output, content_type='application/json')

def announcements(request):
        #filter query
        query = Q()
        
        if request.GET.get('sections'):
                section_codes = request.GET.get('sections').split('-')
                for section_code in section_codes:
                        section = get_object_or_404(Section, id=int(section_code))
                        query.add(Q(to__section=section), Q.OR)
        elif request.GET.get('section_course'):
                course_section_list = request.GET.get('section_course').split('-')
                for course_section in course_section_list:
                        course = get_object_or_404(Course, id=int(course_section.split(':')[-1]))
                        section = get_object_or_404(Section, id=int(course_section.split(':')[0]))
                        query.add(Q(to__section=section,to__course=course), Q.OR)
        else:
                return HttpResponse("Incorrect API request format. Refer to the docmumentaion.")

        # Apply filter
        if request.GET.get('id'):
                announcements = Announcement_To.objects.filter(id__gt=int(request.GET.get('id'))).filter(query).order_by('announcement__pub_date').distinct()
        else:
                announcements = Announcement_To.objects.filter(query).order_by('announcement__pub_date').distinct()

        #JSON output
        #Start json array
        output = "[";

        for announcement in announcements:
                output += "{"
                output += "\"id\":" + str(announcement.id) + ","
                output += "\"message\":" + "\"" + announcement.announcement.message + "\"" + ","
                output += "\"lecturer_name\":" + "\"" + announcement.to.teacher + "\"" + ","
                output += "\"pub_date\":" + str(announcement.announcement.pub_date) + ","
                output += "\"exp_date\":" + str(announcement.announcement.exp_date) + ","
                output += "},"

        # remove the last list separator comma
        output = output[::-1].replace(",", "", 1)[::-1]

        #end of json array
        output += "]"

        for announcement in announcements:
                announcement.announcement.inc_count()
        
        return HttpResponse(output, content_type='application/json')

def materials(request):
        #Filter query
        query = Q()
        
        if request.GET.get('section_course'):
                course_section_list = request.GET.get('section_course').split('-')
                for course_section in course_section_list:
                        course = get_object_or_404(Course, id=int(course_section.split(':')[-1]))
                        section = get_object_or_404(Section, id=int(course_section.split(':')[0]))
                        query.add(Q(to__section=section,to__course=course),Q.OR)
        elif request.GET.get('sections'):
                section_codes = request.GET.get('sections').split('-')
                for section_code in section_codes:
                        section = get_object_or_404(Section, id = int(section_code))
                        query.add(Q(to__section=section),Q.OR)
        else:
                return HttpResponse("Incorrect API request format. Refer to the docmumentaion.")

        #Apply filter
        if request.GET.get('id'):
                materials = Material_To.objects.filter(id__gt=int(request.GET.get('id'))).filter(query).order_by('material.pub_date').distinct()
        else:
                materials = Material_To.objects.filter(query).order_by('material.pub_date').distinct()

        #JSON output
        #Start json array
        output = "[";

        for material in materials:
                output += "{"
                output += "\"id\":" + str(material.id) + ","
                output += "\"name\":" + "\"" + material.material.name + "\"" + ","
                output += "\"description\":" + "\"" + material.material.description + "\"" + ","
                output += "\"pub_date\":" + "\"" + str(material.material.pub_date) + "\"" + ","
                output += "\"file_format\":" + "\"" + material.material.ext() + "\"" + ","
                output += "\"file_size\":" + str(material.material.file_size()) + ","
                output += "\"course_id\":" + str(material.to.course.id)
                output += "},"

        # remove the last list separator comma
        output = output[::-1].replace(",", "", 1)[::-1]

        #end of json array
        output += "]"

        return HttpResponse(output, content_type='application/json')

def section_exists(request):
        section_code = request.GET.get('section_code')

        #JSON output
        #Start json array
        output = "{"
        
        if Section.objects.filter(code=section_code).count() < 1:
                output += " \"status\":false }"
        else:
                output += " \"status\":true }"

        return HttpResponse(output, content_type='application/json')

def sections(request):
        if request.GET.get('department'):
                department = get_object_or_404(Department, id=int(request.GET.get('department')))
                sections = Section.objects.filter(department = department)
        else:
                sections = Section.objects.all()        

        #JSON output
        #Start json array
        output = "["

        for section in sections:
                output += "{"
                output += "\"id\":" + str(section.id) + ","
                output += "\"code\":" + "\"" + section.code + "\""
                output += "},"

        # remove the last list separator comma
        output = output[::-1].replace(",", "", 1)[::-1]

        #end of json array
        output += "]"

        return HttpResponse(output, content_type='application/json')

def departments(request):
        departments = Department.objects.all()
        
        #JSON output
        #Start json array
        output = "["

        for department in departments:
                output += "{"
                output += "\"id\":" + str(department.id) + ","
                output += "\"name\":" + "\"" + department.name + "\"" + ","
                output += "\"code\":" + "\"" + department.code + "\""
                output += "},"

        # remove the last list separator comma
        output = output[::-1].replace(",", "", 1)[::-1]

        #end of json array
        output += "]"

        return HttpResponse(output, content_type='application/json')

def email_exists(request):
        if request.GET.get('email'):
                email = request.GET.get('email')
        else:
                return HttpResponse("Incorrect API request format. Refer to the docmumentaion.")
        
        #JSON output
        #Start json array
        output = "{"        

        if User.objects.filter(username=email).exists():
                output += " \"status\":true }"
        else:
                output += " \"status\":false }"

        return HttpResponse(output, content_type='application/json')
                
def get_courses(request):
        if request.GET.get('department'):
                department_id = int(request.GET.get('department'))
        else :
                return HttpResponse("Incorrect API request format. Refer to the docmumentaion.")
        if request.GET.get('sections'):
                section_codes = request.GET.get('sections').split('-')
                output = "["
                for section_code in section_codes:
                        section = get_object_or_404(Section, id=int(section_code))
                        courses = section.take.filter(department__id = department_id)
                        for course in courses:
                                output += "{"
                                output += "\"id\":" + str(course.id) + ","
                                output += "\"name\":" + "\"" + course.name + "\"" + ","
                                output += "\"section\":" + str(section.id) + ","
                                output += "\"year\":" + str(section.year) + ","
                                output += "\"number\":" + str(section.number)
                                output += "},"                                

                output = output[::-1].replace(",", "", 1)[::-1]
                output += "]"
        else :
                return HttpResponse("Incorrect API request format. Refer to the docmumentaion.")        

        return HttpResponse(output, content_type='application/json')
