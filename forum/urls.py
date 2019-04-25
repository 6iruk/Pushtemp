from django.urls import path, include
from . import views

urlpatterns = [
    path('home/', views.forum_home, name='Forum Home'),
	path('create/', views.forum_create, name="Forum Create"),
	path('feed/', views.forum_feed, name="Forum Feed"),
	path('search/', views.forum_search, name="Forum Search"),
]
