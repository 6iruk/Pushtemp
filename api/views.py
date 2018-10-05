from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.contrib.auth import authenticate, login as auth_login, logout
from django.db.models import Q
from django.contrib.auth.models import User
from main import models

# Create your views here.

def index(request):
        return HttpResponse("Welcome to Push API")

## Returns Educational Institutions
# www.aaupush.com/json/Educational_Institution
def Educational_Institution(request):

    #JSON output
    #Start json array
    output = "["

    # Loop through every Educational Institution and add them as a json object
    for Institution in models.Educational_Institution.objects.all():
        output += "{"
        output += "\"id\":" + str(Institution.id) + ","
        output += "\"name\":" + "\"" + Institution.name + "\"" + ","
        output += "\"country\":" + "\"" + Institution.country + "\"" + ","
        output += "\"city\":" + "\"" + Institution.city + "\"" + ","
        output += "\"ownership_type\":" + "\"" + Institution.ownership_type + "\"" + ","
        output += "\"institution_type\":" + "\"" + Institution.institution_type + "\""
        output += "},"

    # remove the last list separator comma
    output = output[::-1].replace(",", "", 1)[::-1]

    #end of json array
    output += "]"

    return HttpResponse(output, content_type='application/json')


## Returns Departments
# www.aaupush.com/json/Department?by-educational-institution={{Educational_Institution_ID}}
# GET variable is optionl
def Department(request):

    #Check if the api request is based on a specific Educational Institution
    if request.GET.get('by-educational-institution'):

        #Get all departments in that specific Educational_Institution(THE 'ID' ATTRIBUTE SHOULD BE SENT/USED TO SPECIFY THE INSTANCE)
        Departments = models.Department.objects.filter(university_in__id = int(request.GET.get('by-educational-institution')))

    #Get all departments
    else :
        Departments = models.Department.objects.all()


    #JSON output
    #Start json array
    output = "[";

    # Loop through every Department and add them as a json object
    for Department in Departments:
        output += "{"
        output += "\"id\":" + str(Department.id) + ","
        output += "\"university_in\":" + "\"" + Department.university_in.name + "\"" + ","
        output += "\"name\":" + "\"" + Department.name + "\"" + ","
        output += "\"field\":" + "\"" + Department.field + "\""
        output += "},"

    # remove the last list separator comma
    output = output[::-1].replace(",", "", 1)[::-1]

    #end of json array
    output += "]"

    return HttpResponse(output, content_type='application/json')


## Returns Sections
# www.aaupush.com/json/Section?by-educational-institution={{Educational_Institution_ID}}&by-department={{Department_ID}}
# GET variables are optional
def Section(request):

    #Check if the api request is based on a specific Educational Institution
    if request.GET.get('by-educational-institution'):

        #Get all sections in that specific Educational Institution(THE 'ID' ATTRIBUTE SHOULD BE SENT/USED TO SPECIFY THE INSTANCE)
        Sections = models.Section.objects.filter(department_in__university_in__id = int(request.GET.get('by-educational-institution')))

    #Check if the api request is based on a specific Department
    elif request.GET.get('by-department'):

        #Get all sections in that specific Department(THE 'ID' ATTRIBUTE SHOULD BE SENT/USED TO SPECIFY THE INSTANCE)
        Sections = models.Section.objects.filter(department_in__id = int(request.GET.get('by-department')))

    #Get all sections
    else :
        Sections = models.Section.objects.all()


    #JSON output
    #Start json array
    output = "[";

    # Loop through every Section and add them as a json object
    for Section in Sections:
        output += "{"
        output += "\"id\":" + str(Section.id) + ","
        output += "\"department_in\":" + "\"" + Section.department_in.name + "\"" + ","
        output += "\"year\":" + str(Section.year) + ","
        output += "\"section_id\":" + "\"" + Section.section_id + "\"" + ","
        output += "\"section_takes\":" + "["

        # Loop through every course the section takes and add them as a json object
        for Course in Section.section_takes.all():
            output += "{"
            output += "\"id\":" + str(Course.id) + ","
            output += "\"name\":" + "\"" + Course.name + "\"" + ","
            output += "\"course_code\":" + "\"" + Course.course_code + "\"" + ","
            output += "\"module_code\":" + "\"" + Course.module_code + "\"" + ","
            output += "\"given_by\":" + "\"" + Course.given_by.name + "\""
            output += "},"

        if Section.section_takes.all().count() > 0:
            # remove the last list separator comma
            output = output[::-1].replace(",", "", 1)[::-1]

        #Close section_takes array
        output += "]"

        output += "},"

    # remove the last list separator comma
    output = output[::-1].replace(",", "", 1)[::-1]

    #end of json array
    output += "]"

    return HttpResponse(output, content_type='application/json')



## Returns Courses
# www.aaupush.com/json/Course?by-department={{Department_ID}}&by-student={{}}
# The GET variables must be used with every request
def Course(request):

    #Check if the api request is for courses given by a Department
    if request.GET.get('by-department'):

        #Get all courses given by the Department(THE 'ID' ATTRIBUTE SHOULD BE SENT/USED TO SPECIFY THE INSTANCE)
        Courses = models.Course.objects.filter(given_by__id = int(request.GET.get('by-department')))

    #Check if the api request is for courses taken by a student
    elif request.GET.get('by-student'):

        #Get the student instance of the logged in user/student
        student = models.Student.objects.get(user = request.user)

        #Get the ids of the courses the student takes
        ids = student.class_in.values_list('course', flat=True)

        #Get all courses taken by a the student[THE 'ID' ATTRIBUTE ISN'T NEEDED FOR THIS REQUEST, ASSIGN ANY VALUE YOU WANT TO 'by-student']
        Courses = models.Course.objects.filter(pk__in=set(ids))

    #The request wasn't based on department or student, return nothing
    else:
        Courses = {}

    #JSON output
    #Start json array
    output = "["

    # Loop through every Course and add them as a json object
    for Course in Courses:
        output += "{"
        output += "\"id\":" + str(Course.id) + ","
        output += "\"name\":" + "\"" + Course.name + "\"" + ","
        output += "\"course_code\":" + "\"" + Course.course_code + "\"" + ","
        output += "\"module_code\":" + "\"" + Course.module_code + "\"" + ","
        output += "\"given_by\":" + "\"" + Course.given_by.name + "\""
        output += "},"

    # remove the last list separator comma
    output = output[::-1].replace(",", "", 1)[::-1]

    #end of json array
    output += "]"

    return HttpResponse(output, content_type='application/json')



## Returns Posts with ID greater than the specified Post_ID
# www.aaupush.com/json/Post?by-post={{Post_ID}}
# GET variable is a must
def Post(request):

    #Get the student instance of the logged in user/student
    student = models.Student.objects.get(user = request.user)

    #Get the classes the student takes part in
    classes_in = student.class_in.all()

    #A query to filter posts from Post_To_Class
    query = Q()

    #Loop through the classes the student takes to build a query
    for class_in in classes_in:

        #Add every class the student takes to the query
        query.add( Q( post_to = class_in ), Q.OR )

    #A query to filter posts from Post_To_Section
    query2 = Q()

    #Loop through the sections the student is in to build a query
    for section in classes_in:

        #Add every section the student is in to the query
        query2.add( Q( post_to = section.section ), Q.OR )

    #Get class posts
    posts_to_class = models.Post_To_Class.objects.filter(query).filter( post__id__gt = int(request.GET.get('by-post')))

    #Get section posts
    posts_to_section =  models.Post_To_Section.objects.filter(query2).filter( post__id__gt = int(request.GET.get('by-post')))

    #Get student posts
    posts_to_student =  models.Post_To_Student.objects.filter( post_to = student ).filter( post__id__gt = int(request.GET.get('by-post')))

    #Get all the posts and append them
    Posts = list(posts_to_class) + list(posts_to_section) + list(posts_to_student)
    #sorted_things = sorted(all_things, key=lambda x: x.date)


    #JSON output
    #Start json array
    output = "["

    # Loop through every Post and add them as a json object
    for Post in Posts:
        output += "{"
        output += "\"id\":" + str(Post.post.id) + ","
        output += "\"content\":" + "\"" + Post.post.content + "\"" + ","

        #Start json array for Post files
        output += "\"files\":" + "["

        for File in Post.post.files.all():
            output += "{"
            output += "\"id\":" + str(File.id) + ","
            output += "\"name\":" + "\"" + File.name + "\"" + ","
            output += "\"extension\":" + "\"" + File.extension + "\"" + ","
            output += "\"post_by\":" + "\"" + File.post_by.__str__() + "\""
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
            output += "\"post_by\":" + "\"" + Image.post_by.__str__() + "\""
            output += "},"

        if Post.post.images.all().count() > 0:
            # remove the last list separator comma
            output = output[::-1].replace(",", "", 1)[::-1]

        #Close images array
        output += "],"

        output += "\"post_type\":" + str(Post.post.post_type) + ","
        output += "\"post_by\":" + "\"" + Post.post.post_by.__str__() + "\"" + ","
        output += "\"pub_date\":" + str(Post.post.pub_date)
        output += "},"

    # remove the last list separator comma
    output = output[::-1].replace(",", "", 1)[::-1]

    #end of json array
    output += "]"

    return HttpResponse(output, content_type='application/json')



## Returns Reminders with ID greater than the specified Reminder_ID
# www.aaupush.com/json/Reminder?by-reminder={{Reminder_ID}}
# GET variable is a must
def Reminder(request):

    #Get the student instance of the logged in user/student
    student = models.Student.objects.get(user = request.user)

    #Get the classes the student takes part in
    classes_in = models.Student_Takes.objects.filter(student = student)

    #A query to filter posts from Reminder_To_Class
    query = Q()

    #Loop through the classes the student takes to build a query
    for class_in in classes_in:

        #Add every class the student takes to the query
        query.add( Q( reminder_to = class_in.class_in ), Q.OR )

    #Get reminders with ID greater than the specified Reminder_ID
    Reminders = models.Reminder_To_Class.objects.filter(query).filter( id__gt = int(request.GET.get('by-reminder')))


    #JSON output
    #Start json array
    output = "[";

    # Loop through every Course and add them as a json object
    for Reminder in Reminders:
        output += "{"
        output += "\"id\":" + str(Reminder.id) + ","
        output += "\"reminder_for\":" + str(Reminder.reminder_for) + ","
        output += "\"title\":" + "\"" + Reminder.title + "\"" + ","
        output += "\"due_date\":" + str(Reminder.due_date) + ","
        output += "\"due_time\":" + str(Reminder.due_time) + ","
        output += "\"place\":" + "\"" + Reminder.place + "\""
        output += "},"

    # remove the last list separator comma
    output = output[::-1].replace(",", "", 1)[::-1]

    #end of json array
    output += "]"

    return HttpResponse(output, content_type='application/json')



def login(request):
        user = None
        role = ''
        status = ''
        remark = ''

        def staff():
                nonlocal user
                nonlocal role

                staff = models.Staff.objects.get(email = request.POST.get('email'))
                password = request.POST.get('sta_password')
                user = authenticate(username=staff.user.username, password=password)
                role = 'staff'


        def student():
                nonlocal user
                nonlocal role

                student = models.Student.objects.get(reg_id = request.POST.get('reg_id'))
                password = request.POST.get('stu_password')
                user = authenticate(username=student.user.username, password=password)
                role = 'student'


        if (request.POST.get('user-type') == 'staff'):
            staff()
        elif (request.POST.get('user-type') == 'student'):
            student()
        else:
                return HttpResponse("{\"role\":\"null\", \"status\":4, \"remark\":\"User type not found\"}", content_type='application/json')

        def success():
                auth_login(request, user)

                nonlocal status
                nonlocal remark

                status = 1
                remark = 'Authentication success'

        def failure():
                nonlocal status
                nonlocal remark

                status = 0
                remark = 'Authentication failed'

        def notActive():
                nonlocal status
                nonlocal remark

                status = 3
                remark = 'Account not active'

        if user is not None:
                if user.is_active:
                        success()
                else:
                        notActive()
        else:
                failure()


        #JSON output
        #Start json object
        output = "{\"role\":"
        output += "\"" + role + "\","
        output += "\"status\":"
        output +=  str(status) + ","
        output += "\"remark\":"
        output += "\"" + remark + "\"}"

        return HttpResponse(output, content_type='application/json')



def signup(request):
        status = 0
        remark = ""
        fields = []

        first_name = request.POST.get('first-name')
        last_name = request.POST.get('last-name')
        phone = request.POST.get('phone-number')
        email = request.POST.get('email')
        department_in = models.Department.objects.get(id = int(request.POST.get('department')))
        year = int(request.POST.get('year'))
        section = models.Section.objects.get(department_in = department_in, year = year, section_id = request.POST.get('section'))
        reg_id = request.POST.get('reg-id')
        password = request.POST.get('password')

        user = User.objects.create_user(reg_id.replace("/","-"), "", password)
        student = models.Student.objects.create(university_in = department_in.university_in, department_in = department_in, year = year, section = section.section_id, first_name = first_name, last_name = last_name, reg_id = reg_id, phone = phone, email = email, user = user)

        for class_in in models.Instructor_Teaches.objects.filter(section=section):
            student.class_in.add(class_in)

        status = 1
        remark = "Sign up successfull"

        #JSON output
        #Start json object
        output = "{\"status\":"
        output +=  str(status) + ","
        output += "\"remark\":"
        output += "\"" + remark + "\"" + ","
        output += "\"fields\":["

        for field in fields:
            output +=  "\"" + field + "\","

        if len(fields) > 0:
            # remove the last list separator comma
            output = output[::-1].replace(",", "", 1)[::-1]

        output += "]}"

        return HttpResponse(output, content_type='application/json')



def email_exists(request):
        if request.GET.get('email'):
                email = request.GET.get('email')
        else:
                return HttpResponse("Incorrect API request format. Refer to the docmumentaion.")

        #JSON output
        #Start json array
        output = "{"

        if models.Staff.objects.filter(email=email).exists():
                output += " \"status\":true }"

        elif models.Student.objects.filter(email=email).exists():
                output += " \"status\":true }"

        else:
                output += " \"status\":false }"

        return HttpResponse(output, content_type='application/json')



def phone_exists(request):
        if request.GET.get('phone-number'):
                phone = request.GET.get('phone-number')
        else:
                return HttpResponse("Incorrect API request format. Refer to the docmumentaion.")

        #JSON output
        #Start json array
        output = "{"

        if models.Staff.objects.filter(phone = phone).exists():
                output += " \"status\":true }"

        elif models.Student.objects.filter(phone = phone).exists():
                output += " \"status\":true }"

        else:
                output += " \"status\":false }"

        return HttpResponse(output, content_type='application/json')



def reg_id_exists(request):
        if request.GET.get('reg_id'):
                reg_id = request.GET.get('reg_id')
        else:
                return HttpResponse("Incorrect API request format. Refer to the docmumentaion.")

        #JSON output
        #Start json array
        output = "{"

        if models.Student.objects.filter(reg_id = reg_id).exists():
                output += " \"status\":true}"

        else:
                output += " \"status\":false }"

        return HttpResponse(output, content_type='application/json')



def get_latest_app_version(request):

        #JSON output
        #Start json array
        output = "{"

        output += " \"version_name\": \"1.03\" ,"
        output += " \"version_code\": 9 }"

        return HttpResponse(output, content_type='application/json')
