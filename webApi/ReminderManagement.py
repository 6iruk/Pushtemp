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
        output += "\"note\":" + "\"" + Reminder.note + "\"" + ","
        output += "\"due_date\":" + str(Reminder.due_date) + ","
        output += "\"due_time\":" + str(Reminder.due_time) + ","
        output += "\"place\":" + "\"" + Reminder.place + "\""
        output += "},"

    # remove the last list separator comma
    output = output[::-1].replace(",", "", 1)[::-1]

    #end of json array
    output += "]"

    return HttpResponse(output, content_type='application/json')
