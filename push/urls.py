"""push URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from main import views
from forum import views as views2

urlpatterns = [
    path('' ,views.index, name='Home'),
    path('signup/',views.students_signup_page, name='Sign Up'),
    path('login/',views.login_page, name='Log In'),
    path('student/account/' ,views.student_account_page, name='Student Account'),
    path('staff/account/' ,views.staff_account_page, name='Staff Account'),
    path('forum/home', views2.forum_home, name='Forum Home'),
    path('forum/create', views2.forum_create, name="Forum Create"),
    path('forum/feed', views2.forum_feed, name="Forum Feed"),
    path('forum/search', views2.forum_search, name="Forum Search"),
    #path('invite/' ,views.teacher_xls_page, name='XLS'),
    path('first_login/' ,views.first_login, name='First Login'),
    path('Push_Page/', include('pushPages.urls')),
    path('admin/', admin.site.urls),
    path('json/', include('webApi.urls')),
    path('api/forum/', include('forum.urls')),
]
