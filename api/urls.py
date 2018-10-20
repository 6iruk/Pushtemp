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
	url(r'^login$', views.login, name="Login"),
	url(r'^signup$', views.signup, name="Signup"),
	url(r'^account_update$', views.account_update, name="Account Update"),
	url(r'^add_drop$', views.add_drop, name="Add-Drop"),
    url(r'^email_exists$', views.email_exists, name="Email exists"),
	url(r'^phone_exists$', views.phone_exists, name="Phone exists"),
	url(r'^reg_id_exists$', views.reg_id_exists, name="Reg_ID exists"),
    url(r'^get_latest_app_version$', views.get_latest_app_version, name="get_latest_app_version"),
]
