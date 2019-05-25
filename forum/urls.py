from django.urls import path
from . import views

urlpatterns = [
	path('forumlist', views.forums_user_is_in, name='Forum List'),
	path('trendingforums/', views.trending_forums, name="Trending Forums"),
	path('forummessages/', views.forum_posts, name="Forum Messages"),
	path('sendmessage/', views.send_message, name="Send Message"),
	path('joinforum/', views.join_forum, name="Join Forum"),
	path('leaveforum/', views.leave_forum, name="Leave Forum"),
	path('createforum/', views.create_forum, name="Create Forum"),
	path('deleteforum/', views.delete_forum, name="Delete Forum"),
]
