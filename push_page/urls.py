from django.conf.urls import url , include
from . import views

urlpatterns = [
    url('^(?P<push_page>[0-9a-zA-z]+)/$',views.Push_Page, name='Push_Page'),
    ]
