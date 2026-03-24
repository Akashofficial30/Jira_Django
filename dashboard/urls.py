from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),  # homepage
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('projects/', views.projects_view, name='projects'),
    path('tasks/', views.tasks_view, name='tasks'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('update-status/<int:task_id>/', views.update_status, name='update_status'),
    path('projects/<int:project_id>/', views.project_detail_view, name='project_detail'),
]