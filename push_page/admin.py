from django.contrib import admin
from .models import *

# Register your models here.

models = {PushPage,Post,Picture}

for model in models:
    admin.site.register(model)





    

