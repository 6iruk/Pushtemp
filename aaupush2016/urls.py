"""aaupush2016 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url , include
from django.contrib import admin
from main import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    url(r'^$' ,views.index, name='Home'),
    url(r'^signup/$',views.students_signup_page, name='Sign Up'),
    url(r'^login/$',views.login_page, name='Log In'),
    url(r'^student/account$' ,views.student_account_page, name='Student Account'),
    url(r'^staff/account$' ,views.staff_account_page, name='Staff Account'),
    # url(r'^section/', include('main.urls')),
    # url(r'^file/(?P<material_id>[0-9a-zA-Z]+)/$',views.file_request, name='File'),
    # url(r'^forgot_password/$',views.forgot_password, name='forgot_password'),
    # url(r'^portal/$',views.portal, name='portal'),
    # url(r'^first_login/$',views.first_login, name='first_login'),
    url(r'^Push_Page/', include('push_page.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^json/', include('api.urls')),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
