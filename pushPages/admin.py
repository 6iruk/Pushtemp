from django.contrib import admin
from .models import *


models = {PushPage,Post,Picture}

for model in models:
    admin.site.register(model)
