from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

app_name ="students"

urlpatterns = [
    # student urls
    path('student/', student_register, name='student_register'),
    path('', student_login, name='student_login'),
    path('dashboard/', student_dashboard, name='student_dashboard'),
    path('profile/', student_profile, name='student_profile'),

    # register urls
    path('register/login/', registrar_login, name='registrar_login'),
    path('register/dashboard/', registrar_dashboard, name='registrar_dashboard'),
    path('register/delete/<int:student_id>/', delete_student, name='delete_student'),

    # logout
    path('logout/', student_logout, name='logout')
    # path('logout/', auth_views.LogoutView.as_view(), name='logout')
]