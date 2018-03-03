from django.conf.urls import url , include
from . import views
urlpatterns = [
  url('^(?P<section_code>.+)/(?P<course_name>.+)/$', views.course_view, name='course_view'),
  url('^(?P<section_code>.+)/$', views.section, name='Section'),
]
