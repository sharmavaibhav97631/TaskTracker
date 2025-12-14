from django.urls import path
from . import views
from django.shortcuts import redirect

def home(request):
    return redirect("/projects/")

urlpatterns = [
    path("", home, name="home"),
    path("projects/", views.projects_view, name="projects"),
    path("projects/<int:project_id>/tasks/", views.create_task, name="create_task"),
    path("tasks/", views.tasks_list, name="tasks"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
]
