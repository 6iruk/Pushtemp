## Returns Posts with ID greater than the specified Post_ID
# www.aaupush.com/json/Post?by-post={{Post_ID}}
# GET variable is a must
def Post(request):

    Posts = []

    #Get the student instance of the logged in user/student
    student = models.Student.objects.get(user = request.user)

    #Get the classes the student takes part in
    classes_in = student.class_in.all()

    #A query to filter posts
    query = Q()

    if request.GET.get('by-type') == "wall":
        #Loop through the classes the student takes to build a query
        for class_in in classes_in:

            #Add every class the student takes to the query
            query.add( Q( post_to = class_in ), Q.OR )

        if request.GET.get('by-class-post'):
            Posts = models.Post_To_Class.objects.filter( post__id__gt = int(request.GET.get('by-class-post'))).filter(query)

        elif request.GET.get('by-student-post'):
            Posts = models.Post_To_Student.objects.filter( post__id__gt = int(request.GET.get('by-student-post'))).filter(query)

        elif request.GET.get('by-page'):
            posts_to_class = models.Post_To_Class.objects.filter(query)
            posts_to_student = models.Post_To_Student.objects.filter( post_to = student )

            Posts = sorted((list(posts_to_class) + list(posts_to_student)), key=lambda x: x.post.pub_date)

        else :
            posts_to_class = models.Post_To_Class.objects.filter(query)
            posts_to_student = models.Post_To_Student.objects.filter( post_to = student )

            Posts = sorted((list(posts_to_class) + list(posts_to_student)), key=lambda x: x.post.pub_date)

    elif request.GET.get('by-type') == "pushboard":
        #Loop through the sections the student is in to build a query
        for section in classes_in:

            #Add every section the student is in to the query
            query.add( Q( post_to = section.section ), Q.OR )

        if request.GET.get('by-section-post'):
            Posts = models.Post_To_Section.objects.filter( post__id__gt = int(request.GET.get('by-section-post'))).filter(query)

        elif request.GET.get('by-page'):
            Posts = models.Post_To_Section.objects.filter(query)

        else :
            Posts = models.Post_To_Section.objects.filter(query)

    elif request.GET.get('by-type') == "class-post-list":
        if request.GET.get('by-class') and student.class_in.filter(id = int(request.GET.get('by-class'))).exists():
            posts = models.Post_To_Class.objects.filter(post_to = student.class_in.get(id = int(request.GET.get('by-class')))).exclude(post__files = None)

        context = {'posts':posts}
        return render(request, 'main/class-posts-snippet.html', context)

    elif request.GET.get('by-type') == "miscellaneous":
        for section in classes_in:

            #Add every section the student is in to the query
            query.add( Q( post_to = section.section ), Q.OR )

        posts_to_section = models.Post_To_Section.objects.filter(query)
        posts_to_student = models.Post_To_Student.objects.filter( post_to = student )

        posts = sorted((list(posts_to_section) + list(posts_to_student)), key=lambda x: x.post.pub_date)
        context = {'posts':posts}
        return render(request, 'main/class-posts-snippet.html', context)
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



def post_action(request):
        if not request.user.is_authenticated:
            return HttpResponse("{\"status\":3, \"remark\":\"User not authenticated\"}", content_type='application/json')

        if models.Staff.objects.filter(user=request.user).exists():
            staff = models.Staff.objects.get(user=request.user)

        else:
            return HttpResponse("{\"status\":2, \"remark\":\"Staff not found\"}", content_type='application/json')


        if request.POST.get('action-type') == "chat":
            if not request.POST.get('post-content') or (request.POST.get('post-content').strip() == ""):
                    return HttpResponse("{\"status\":0, \"remark\":\"Content not found\", \"id\":\"#group-chat-post-content-error\", \"html\":\"<span>Post content is required</span>\"}", content_type='application/json')

            if request.FILES.get('image-1'):
                if request.FILES['image-1'].name.split('.')[-1].strip().lower() not in ["jpeg","jpg","gif","png","bmp","svg"]:
                    return HttpResponse("{\"status\":0, \"remark\":\"File name not found\",  \"id\":\"#group-chat-attachment-error\", \"html\":\"<span>Image format not supported</span>\"}", content_type='application/json')


            content = request.POST.get('post-content')
            pub_date = datetime.datetime.now()

            post = models.Post.objects.create(content = content, post_type = 4, post_by = staff, pub_date = pub_date)

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

            return HttpResponse("{\"status\":1, \"remark\":\"Post Successful\", \"html\":\"" + html + "\"}", content_type='application/json')


        if (request.POST.get('post-content').strip() == ""):
                return HttpResponse("{\"status\":0, \"remark\":\"Content not found\", \"id\":\"#post-content-error\", \"html\":\"<span>Post content is required</span>\"}", content_type='application/json')

        if not request.POST.getlist('section-recipients'):
            if not request.POST.getlist('class-recipients'):
                return HttpResponse("{\"status\":0, \"remark\":\"Recipient not found\", \"id\":\"#post-recipient-error\", \"html\":\"<span>Choose at least one post recipient</span>\"}", content_type='application/json')

        if request.FILES.get('file-1'):
            if request.POST.get('file-name-1').strip() == "":
                return HttpResponse("{\"status\":0, \"remark\":\"File name not found\", \"id\":\"#post-file-1-error\", \"html\":\"<span>File name is required</span>\"}", content_type='application/json')

        if request.FILES.get('file-2'):
            if request.POST.get('file-name-2').strip() == "":
                return HttpResponse("{\"status\":0, \"remark\":\"File name not found\",  \"id\":\"#post-file-2-error\", \"html\":\"<span>File name is required</span>\"}", content_type='application/json')

        if request.FILES.get('file-3'):
            if request.POST.get('file-name-3').strip() == "":
                return HttpResponse("{\"status\":0, \"remark\":\"File name not found\",  \"id\":\"#post-file-3-error\", \"html\":\"<span>File name is required</span>\"}", content_type='application/json')

        if request.FILES.get('image-1'):
            if request.FILES['image-1'].name.split('.')[-1].strip().lower() not in ["jpeg","jpg","gif","png","bmp","svg"]:
                return HttpResponse("{\"status\":0, \"remark\":\"Image format not supported\",  \"id\":\"#post-image-1-error\", \"html\":\"<span>Image format not supported</span>\"}", content_type='application/json')

        if request.FILES.get('image-2'):
                if request.FILES['image-2'].name.split('.')[-1].strip().lower() not in ["jpeg","jpg","gif","png","bmp","svg"]:
                    return HttpResponse("{\"status\":0, \"remark\":\"Image format not supported\",  \"id\":\"#post-image-2-error\", \"html\":\"<span>Image format not supported</span>\"}", content_type='application/json')

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
                    file = models.File.objects.create(file = request.FILES.get('file-1'), name = name, extension = request.FILES['file-1'].name.split('.')[-1], post_by = staff.user)
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



        status = 1
        remark = "Action successul"



        #JSON output
        #Start json object
        output = "{\"status\":"
        output +=  str(status) + ","
        output += "\"remark\":"
        output += "\"" + remark + "\"}"


        return HttpResponse(output, content_type='application/json')


def edit_post(request):
    post = Post.objects.get(id = int(request.POST.get('post-id')))
    post.content = request.POST.get('content')
    post.save()

    return HttpResponse("{\"status\":1, \"remark\":\"Edit successful\"}", content_type='application/json')


def delete_post(request):
    post = Post.objects.get(id = int(request.GET.get('post-id')))
    post.delete()

    return HttpResponse("{\"status\":1, \"remark\":\"Edit successful\"}", content_type='application/json')


def student_read(request):
        if not request.user.is_authenticated:
            return HttpResponse("{\"status\":3, \"remark\":\"User not authenticated\"}", content_type='application/json')

        if models.Student.objects.filter(user=request.user).exists():
            student = models.Student.objects.get(user=request.user)

        else:
            return HttpResponse("{\"status\":2, \"remark\":\"Student not found\"}", content_type='application/json')

        if not request.POST.get("post") or request.POST.get("post").strip() == "":
            return HttpResponse("{\"status\":0, \"remark\":\"Post not sent\"}", content_type='application/json')

        if models.Post.objects.filter(id = int(request.POST.get("post"))).exists():
            post = models.Post.objects.get(id = int(request.POST.get("post")))

        else:
            return HttpResponse("{\"status\":0, \"remark\":\"Post doesn't exist\"}", content_type='application/json')

        if models.Tracking.objects.filter(student = student, post = post, status = 1).exists():
            info = models.Tracking.objects.get(student = student, post = post, status = 1)
            info.status = 2
            info.read_on = datetime.datetime.now()
            info.save()

        return HttpResponse("{\"status\":1, \"remark\":\"Successful\"}", content_type='application/json')
