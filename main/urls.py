from django.conf.urls import url , include
from . import views
urlpatterns = [
  url('^(?P<section_code>[0-9a-zA-Z]+)/$', views.section, name='Section'),
  url('^(?P<section_code>[0-9a-zA-Z]+)/(?P<course_name>.+)/$', views.course_view, name='course_view'),
]
