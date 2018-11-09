from django.urls import path, include
from . import views

urlpatterns = [
	path('', views.index, name='API_Index'),
        path('Educational_Institution/', views.Educational_Institution, name='API_Educational_Institution'),
	path('Department/', views.Department, name="API_Department"),
	path('Section/', views.Section, name="API_Section"),
	path('Course/', views.Course, name="API_Course"),
	path('Post/', views.Post, name="API_Post"),
	path('Reminder/', views.Reminder, name="API_Reminder"),
	path('login/', views.login, name="API_Login"),
	path('signup/', views.signup, name="API_Signup"),
	path('account_update/', views.account_update, name="API_Account Update"),
	path('add_drop/', views.add_drop, name="API_Add-Drop"),
	path('post_action/', views.post_action, name="API_Post Action"),
	path('student_read/', views.student_read, name="API_Student_Read"),
    path('email_exists/', views.email_exists, name="API_Email exists"),
	path('phone_exists/', views.phone_exists, name="API_Phone exists"),
	path('reg_id_exists/', views.reg_id_exists, name="API_Reg_ID exists"),
    path('get_latest_app_version/', views.get_latest_app_version, name="API_get_latest_app_version"),
]
