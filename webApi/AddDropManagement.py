def add_drop(request):
        action = ""
        no_of_courses = 0
        html = ""
        course = ""
        drop_class_id = -1
        role = ""
        student = None
        staff = None

        if not request.user.is_authenticated:
            return HttpResponse("{\"action\":\"null\", \"status\":2, \"remark\":\"User not authenticated\"}", content_type='application/json')

        if models.Student.objects.filter(user=request.user).exists():
            student = models.Student.objects.get(user=request.user)
            role = 'student'

        elif models.Staff.objects.filter(user=request.user).exists():
            staff = models.Staff.objects.get(user=request.user)
            role = 'staff'

        else:
            return HttpResponse("{\"action\":\"null\", \"status\":3, \"remark\":\"User not found\"}", content_type='application/json')


        if request.POST.get('action_type') == "add":
            action = "add"
            classes_id = request.POST.getlist('class')

            if student:
                for class_id in classes_id:
                    pair = class_id.split('-')

                    if not models.Instructor_Teaches.objects.filter(section__id = int(pair[0]), course_id = int(pair[1])).exists():
                        models.Instructor_Teaches.objects.create(section = models.Section.objects.get(id = int(pair[0])), course = models.Course.objects.get(id = int(pair[1])))

                    class_obj = models.Instructor_Teaches.objects.filter(section__id = int(pair[0]), course_id = int(pair[1])).order_by('id').first()

                    if not student.class_in.filter(id = class_obj.id).exists():
                        student.class_in.add(class_obj)

                        html += "<tr class='row-" + str(class_obj.id) + "'>"
                        html += "<td>" + class_obj.course.name  + "</td>"
                        html += "<td>" + class_obj.section.department_in.name  + "</td>"
                        html += "<td>Year " + str(class_obj.section.year) + " <br/>Section " + class_obj.section.section_id + "</td>"
                        html += "<td><button class='btn btn-block' type='button' onclick='drop_course(" + str(class_obj.id) + ")'>Drop Course</button></td>"
                        html += "</tr>"

                        no_of_courses += 1

            elif staff:
                for class_id in classes_id:
                    pair = class_id.split('-')

                    if not models.Instructor_Teaches.objects.filter(section__id = int(pair[0]), course_id = int(pair[1])).exists():
                        models.Instructor_Teaches.objects.create(section = models.Section.objects.get(id = int(pair[0])), course = models.Course.objects.get(id = int(pair[1])))

                    class_obj = models.Instructor_Teaches.objects.filter(section__id = int(pair[0]), course_id = int(pair[1])).order_by('id').first()

                    if not class_obj.instructor.filter(id = staff.id).exists():
                        class_obj.instructor.add(staff)

                        html += "<tr class='row-" + str(class_obj.id) + "'>"
                        html += "<td>" + class_obj.course.name  + "</td>"
                        html += "<td>" + class_obj.section.department_in.name  + "</td>"
                        html += "<td>Year " + str(class_obj.section.year) + " <br/>Section " + class_obj.section.section_id + "</td>"
                        html += "<td><button class='btn btn-block' type='button' onclick='drop_course(" + str(class_obj.id) + ")'>Drop Course</button></td>"
                        html += "</tr>"

                        no_of_courses += 1


        elif request.POST.get('action_type') == "drop":
            action = "drop"
            class_id = request.POST.get('class')

            if student:
                role = 'student'
                if student.class_in.filter(id = int(class_id)).exists():
                    class_obj = models.Instructor_Teaches.objects.get(id = int(class_id))
                    course = class_obj.course.name
                    drop_class_id = class_obj.id

                    student.class_in.remove(class_obj)

            elif staff:
                role = 'staff'
                class_obj = models.Instructor_Teaches.objects.get(id = int(class_id))

                if class_obj.instructor.filter(id = staff.id).exists():
                    course = class_obj.course.name
                    drop_class_id = class_obj.id

                    class_obj.instructor.remove(staff)
        else:
                return HttpResponse("{\"action\":\"null\", \"status\":4, \"remark\":\"Action not found\"}", content_type='application/json')


        if len(request.POST.getlist('class')) > 0:
            status = 1
            remark = "Action successul"

        else:
            status = 0
            remark = "No classes sent"
            action = "null"


        #JSON output
        #Start json object
        output = "{\"status\":"
        output +=  str(status) + ","
        output += "\"remark\":"
        output += "\"" + remark + "\"" + ","

        if action == "add":
            output += "\"count\":"
            output +=  str(no_of_courses) + ","
            output += "\"html\":"
            output += "\"" + html + "\"" + ","

        else:
            output += "\"course\":"
            output +=  "\"" + course + "\"" + ","
            output += "\"class_id\":"
            output +=  str(drop_class_id) + ","
        output += "\"role\":"
        output += "\"" + role + "\"" + ","
        output += "\"action\":"
        output += "\"" + action + "\"}"

        return HttpResponse(output, content_type='application/json')