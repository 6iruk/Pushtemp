from django.conf.urls import url

from . import views

# Url patterns
urlpatterns = [
	url(r'^$', views.index, name='index'),
    url(r'^Educational_Institution$', views.Educational_Institution, name='Educational_Institution'),
	url(r'^Department$', views.Department, name="Department"),
	url(r'^Section$', views.Section, name="Section"),
	url(r'^Course$', views.Course, name="Course"),
	url(r'^Post$', views.Post, name="Post"),
	url(r'^Reminder$', views.Reminder, name="Reminder"),
    url(r'^email_exists$', views.email_exists, name="email_exists"),
    url(r'^get_latest_app_version$', views.get_latest_app_version, name="get_latest_app_version"),
]
