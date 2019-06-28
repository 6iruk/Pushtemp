def login(request):
        user = None
        role = ''
        status = ''
        remark = ''

        if (request.POST.get('user-type') == 'staff'):
            if not request.POST.get('email') or request.POST.get('email').strip() == "":
                return HttpResponse("{\"role\":\"staff\", \"status\":2, \"id\":\"email-error\", \"html\":\"<span>Email required</span>\"}", content_type='application/json')

            if not request.POST.get('password') or request.POST.get('password').strip() == "":
                return HttpResponse("{\"role\":\"staff\", \"status\":2, \"id\":\"staff-password-error\", \"html\":\"<span>Password required</span>\"}", content_type='application/json')

            if not models.Staff.objects.filter(email = request.POST.get('email')).exists():
                if models.User.objects.filter(username =request.POST.get('email')).exists() and not models.Student.objects.filter(user = models.User.objects.get(username =request.POST.get('email'))).exists():
                    if models.User.objects.get(username =request.POST.get('email')).email == "staff@aau.com":
                        if authenticate(username=request.POST.get('email'), password=request.POST.get('password')) is not None:
                            auth_login(request, models.User.objects.get(username =request.POST.get('email')))
                            return HttpResponse("{\"role\":\"staff\", \"status\":5, \"remark\":\"Go to first login\"}", content_type='application/json')

                return HttpResponse("{\"role\":\"staff\", \"status\":0, \"remark\":\"Authentication failed\"}", content_type='application/json')

            staff = models.Staff.objects.get(email = request.POST.get('email'))
            password = request.POST.get('password')
            user = authenticate(username=staff.user.username, password=password)
            role = 'staff'

        elif (request.POST.get('user-type') == 'student'):
            if not request.POST.get('reg-id') or request.POST.get('reg-id').strip() == "":
                return HttpResponse("{\"role\":\"student\", \"status\":2, \"id\":\"reg-id-error\", \"html\":\"<span>Registration ID required</span>\"}", content_type='application/json')

            if not request.POST.get('password') or request.POST.get('password').strip() == "":
                return HttpResponse("{\"role\":\"student\", \"status\":2, \"id\":\"student-password-error\", \"html\":\"<span>Password required</span>\"}", content_type='application/json')

            if not models.Student.objects.filter(reg_id = request.POST.get('reg-id')).exists():
                return HttpResponse("{\"role\":\"student\", \"status\":0, \"remark\":\"Authentication failed\"}", content_type='application/json')

            student = models.Student.objects.get(reg_id = request.POST.get('reg-id'))
            password = request.POST.get('password')
            user = authenticate(username=student.user.username, password=password)
            role = 'student'

        else:
                return HttpResponse("{\"role\":\"null\", \"status\":4, \"remark\":\"User type not found\"}", content_type='application/json')


        if user is not None:
                if user.is_active:
                        auth_login(request, user)

                        status = 1
                        remark = 'Authentication success'
                else:
                        status = 3
                        remark = 'Account not active'
        else:
                status = 0
                remark = 'Authentication failed'


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

        if not request.POST.get('first-name') or (request.POST.get('first-name').strip() == ""):
            return HttpResponse("{\"status\":0, \"remark\":\"First name required\"}", content_type='application/json')

        if not request.POST.get('last-name') or (request.POST.get('last-name').strip() == ""):
            return HttpResponse("{\"status\":0, \"remark\":\"Last name required\"}", content_type='application/json')

        if not request.POST.get('phone-number') or (request.POST.get('phone-number').strip() == ""):
            return HttpResponse("{\"status\":0, \"remark\":\"Phone number required\"}", content_type='application/json')

        if not request.POST.get('phone-number').startswith("09") and not request.POST.get('phone-number').startswith("251") and not request.POST.get('phone-number').startswith("+251"):
            return HttpResponse("{\"status\":0, \"remark\":\"Phone number format not correct\"}", content_type='application/json')

        if not request.POST.get('phone-number').isdigit():
            return HttpResponse("{\"status\":0, \"remark\":\"Phone number format not correct\"}", content_type='application/json')

        if request.POST.get('email') and request.POST.get('email').strip() != "":
            e = request.POST.get('email')
            if (e.strip().rfind('.') == -1 or e.strip().rfind('@') == -1 or (e.strip().rfind('.') <= e.strip().rfind('@'))):
                return HttpResponse("{\"status\":0, \"remark\":\"Email not valid\"}", content_type='application/json')

        if not request.POST.get('department') or not models.Department.objects.filter(id = int(request.POST.get('department'))).exists():
            return HttpResponse("{\"status\":0, \"remark\":\"Valid department ID required\"}", content_type='application/json')

        if not request.POST.get('year') or (request.POST.get('year').strip() == "") :
            return HttpResponse("{\"status\":0, \"remark\":\"Year required\"}", content_type='application/json')

        if not request.POST.get('year').split('-')[-1].isdigit() or not models.Section.objects.filter(department_in = models.Department.objects.get(id = int(request.POST.get('department'))), year = int(request.POST.get('year').split('-')[-1])).exists():
            return HttpResponse("{\"status\":0, \"remark\":\"Year doesn't exist\"}", content_type='application/json')

        if not request.POST.get('section') or request.POST.get('section').strip() == "":
            return HttpResponse("{\"status\":0, \"remark\":\"Section required\"}", content_type='application/json')

        if not models.Section.objects.filter(department_in = models.Department.objects.get(id = int(request.POST.get('department'))), year = int(request.POST.get('year').split('-')[-1]), section_id = request.POST.get('section')).exists():
            return HttpResponse("{\"status\":0, \"remark\":\"Section not found\"}", content_type='application/json')

        if not request.POST.get('reg-id') or (request.POST.get('reg-id').strip() == ""):
            return HttpResponse("{\"status\":0, \"remark\":\"Registration ID required\"}", content_type='application/json')

        if len(request.POST.get('reg-id').split('/')) != 3 or request.POST.get('reg-id').split('/')[0].upper() != "NSR" or not request.POST.get('reg-id').split('/')[1].isdigit() or not request.POST.get('reg-id').split('/')[2].isdigit():
            return HttpResponse("{\"status\":0, \"remark\":\"ID not correct\"}", content_type='application/json')

        if User.objects.filter(username = request.POST.get('reg-id').replace("/","-")).exists():
            return HttpResponse("{\"status\":0, \"remark\":\"ID already in use\"}", content_type='application/json')

        if not request.POST.get('password') or (request.POST.get('password').strip() == "") or len(request.POST.get('password')) < 7:
            return HttpResponse("{\"status\":0, \"remark\":\"Password must contain more than 7 letters or numbers\"}", content_type='application/json')

        first_name = request.POST.get('first-name')
        last_name = request.POST.get('last-name')
        phone = request.POST.get('phone-number')

        if request.POST.get('email'):
            email = request.POST.get('email')

        else:
            email = ""

        department_in = models.Department.objects.get(id = int(request.POST.get('department')))
        year = int(request.POST.get('year').split('-')[-1])
        section = models.Section.objects.get(department_in = department_in, year = year, section_id = request.POST.get('section'))
        reg_id = request.POST.get('reg-id')
        password = request.POST.get('password')

        user = User.objects.create_user(reg_id.replace("/","-"), "", password)
        student = models.Student.objects.create(university_in = department_in.university_in, department_in = department_in, year = year, section = section.section_id, first_name = first_name, last_name = last_name, reg_id = reg_id, phone = phone, email = email, user = user)

        for course in section.section_takes.all():
            if not models.Instructor_Teaches.objects.filter(section = section, course = course).exists():
                models.Instructor_Teaches.objects.create(section = section, course = course)

            class_in = models.Instructor_Teaches.objects.get(section = section, course = course)
            student.class_in.add(class_in)

        status = 1
        remark = "Sign up successfull"


        #JSON output
        #Start json object
        output = "{\"status\":"
        output +=  str(status) + ","
        output += "\"remark\":"
        output += "\"" + remark + "\"}"

        return HttpResponse(output, content_type='application/json')



def account_update(request):
        status = 0
        remark = ""
        fields = []
        role = ""
        password = request.POST.get('password')

        if not request.user.is_authenticated:
            return HttpResponse("{\"role\":\"null\", \"status\":4, \"remark\":\"User not authenticated\"}", content_type='application/json')

        if not authenticate(username=request.user.username, password=password):
            return HttpResponse("{\"status\":0, \"id\":\"error-password\", \"html\":\"<span>Password not correct</span>\"}", content_type='application/json')

        if not request.POST.get('first-name') or (request.POST.get('first-name').strip() == ""):
            return HttpResponse("{\"status\":0, \"id\":\"error-firstname\", \"html\":\"<span>First name required</span>\"}", content_type='application/json')

        if not request.POST.get('last-name') or (request.POST.get('last-name').strip() == ""):
            return HttpResponse("{\"status\":0, \"id\":\"error-lastname\", \"html\":\"<span>Last name required</span>\"}", content_type='application/json')

        first_name = request.POST.get('first-name')
        last_name = request.POST.get('last-name')

        if request.POST.get('user-type') == "staff":
                if not request.POST.get('email') or (request.POST.get('email').strip() == ""):
                    return HttpResponse("{\"status\":0, \"id\":\"error-email\", \"html\":\"<span>Email required</span>\"}", content_type='application/json')

                if not request.POST.get('title') or (request.POST.get('title').strip() == ""):
                    return HttpResponse("{\"status\":0, \"id\":\"error-title\", \"html\":\"<span>Title required</span>\"}", content_type='application/json')

                if request.POST.get('phone-number') and (request.POST.get('phone-number').strip() == ""):
                    return HttpResponse("{\"status\":0, \"id\":\"error-phonenum\", \"html\":\"<span>Phone not valid</span>\"}", content_type='application/json')

                title = request.POST.get('title')
                email = request.POST.get('email')

                if request.POST.get('phone-number'):
                    phone = request.POST.get('phone-number')

                else:
                    phone = ""

                if models.Staff.objects.filter(user=request.user).exists():
                    staff = models.Staff.objects.get(user = request.user)
                else:
                    return HttpResponse("{\"role\":\"staff\", \"status\":2, \"remark\":\"Staff not found\"}", content_type='application/json')


                staff.title = title
                staff.first_name =  first_name
                staff.last_name = last_name
                staff.phone = phone

                staff.email = email
                user = models.User.objects.get(id = request.user.id)
                user.username = email

                staff.save()
                user.save()

                status = 1
                remark = "Update successful"
                role = "staff"

        elif request.POST.get('user-type') == "student":
                if not request.POST.get('phone-number') or (request.POST.get('phone-number').strip() == ""):
                    return HttpResponse("{\"status\":0, \"id\":\"error-phonenum\", \"html\":\"<span>Phone number required</span>\"}", content_type='application/json')

                if not request.POST.get('year') or (request.POST.get('year').strip() == "") :
                    return HttpResponse("{\"status\":0, \"id\":\"error-year\", \"html\":\"<span>Year required</span>\"}", content_type='application/json')

                if not request.POST.get('year').split('-')[-1].isdigit() or not models.Section.objects.filter(department_in = models.Department.objects.get(id = int(request.POST.get('department'))), year = int(request.POST.get('year').split('-')[-1])).exists():
                    return HttpResponse("{\"status\":0, \"id\":\"error-year\", \"html\":\"<span>Year doesn't exist</span>\"}", content_type='application/json')

                if not request.POST.get('section') or request.POST.get('section').strip() == "":
                    return HttpResponse("{\"status\":0, \"id\":\"error-section\", \"html\":\"<span>Section required</span>\"}", content_type='application/json')

                if not models.Section.objects.filter(department_in = models.Department.objects.get(id = int(request.POST.get('department'))), year = int(request.POST.get('year').split('-')[-1]), section_id = request.POST.get('section')).exists():
                    return HttpResponse("{\"status\":0, \"id\":\"error-section\", \"html\":\"<span>Section not found</span>\"}", content_type='application/json')

                if request.POST.get('email') and (request.POST.get('email').strip() == ""):
                    return HttpResponse("{\"status\":0, \"id\":\"error-email\", \"html\":\"<span>Email not valid</span>\"}", content_type='application/json')

                year = int(request.POST.get('year'))
                section = request.POST.get('section')
                phone = request.POST.get('phone-number')

                if request.POST.get('email'):
                    email = request.POST.get('email')

                else:
                    email = ""

                if models.Student.objects.filter(user=request.user).exists():
                    student = models.Student.objects.get(user = request.user)
                else:
                    return HttpResponse("{\"role\":\"student\", \"status\":2, \"remark\":\"Student not found\"}", content_type='application/json')



                student.year = year
                student.section = section
                student.first_name =  first_name
                student.last_name = last_name
                student.phone = phone
                student.email = email

                student.save()


                status = 1
                remark = "Update successful"
                role = "student"

        else:
                return HttpResponse("{\"role\":\"null\", \"status\":3, \"remark\":\"User type not found\"}", content_type='application/json')


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

        output += "],"
        output += "\"role\":"
        output += "\"" + role + "\"}"

        return HttpResponse(output, content_type='application/json')
        