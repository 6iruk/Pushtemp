from django.urls import path, include
from . import views

urlpatterns = [
	path('login/', views.login, name="Mobile_Login"),
	path('signup/', views.signup, name="Mobile_Signup"),
	path('posts/', views.your_wall_post, name="Mobile_Your_Posts"),
	path('readpost/', views.student_click_read, name="Mobile_Read"),
	path('pushboard/', views.pushboard_post, name="Mobile_Push_Posts"),
	path('reminders/', views.reminders, name="Mobile_Reminders"),
	path('courses/', views.course, name="Mobile_Courses"),
	path('myforums/', views.course, name="Mobile_My_Forums"),
	path('forumsendmessage/', views.send_forum_message, name="Mobile_Forum_Messages"),

	path('postaction/', views.post_action, name="Mobile_Post_action"),
	path('listclasses/', views.class_list, name="Mobile_Class_List"),
]
