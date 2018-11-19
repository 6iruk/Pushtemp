from django.shortcuts import render
from .models import *

def Push_Page(request,push_page):
    page = PushPage.objects.get(event=push_page)
    page_template = page.template
    
    context = {'page':page}
    return render(request,'push_page/%s'%page_template,context)
