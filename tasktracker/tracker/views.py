from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.contrib import messages
from django.db import IntegrityError

from .models import Project, Task

@login_required
def projects_view(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        description = request.POST.get("description")

        if not name:
            messages.error(request, "Project name is required")
            return redirect("/projects/")

        if Project.objects.filter(owner=request.user, name=name).exists():
            messages.error(request, "You already have a project with this name.")
            return redirect("/projects/")

        try:
            Project.objects.create(
                name=name,
                description=description,
                owner=request.user
            )
        except IntegrityError:
            messages.error(request, "Duplicate project name for this user.")
            return redirect("/projects/")

        messages.success(request, "Project created successfully!")
        return redirect("/projects/")

    search = request.GET.get("search")
    qs = Project.objects.filter(owner=request.user)

    if search:
        qs = qs.filter(name__icontains=search)

    return render(request, "tracker/projects.html", {"projects": qs})


@login_required
def create_task(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if project.owner != request.user:
        return HttpResponseForbidden("Not allowed")

    if request.method == "POST":
        try:
            priority = int(request.POST.get("priority"))

            if not 1 <= priority <= 5:
                raise ValueError(
                    "Priority must be between 1 (highest) and 5 (lowest)."
                )

            assignee_id = request.POST.get("assignee_id") or None

            Task.objects.create(
                project=project,
                title=request.POST.get("title"),
                description=request.POST.get("description"),
                priority=priority,
                status=request.POST.get("status", "todo"),
                due_date=request.POST.get("due_date") or None,
                assignee_id=assignee_id,
            )

            messages.success(request, "Task created successfully!")

        except ValueError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, "Invalid task data")

        return redirect("/projects/")

    return redirect("/projects/")


@login_required
def tasks_list(request):
    qs = Task.objects.filter(
        Q(project__owner=request.user) | Q(assignee=request.user)
    ).distinct()

    if status := request.GET.get("status"):
        qs = qs.filter(status=status)

    if project_id := request.GET.get("project_id"):
        qs = qs.filter(project_id=project_id)

    if due_before := request.GET.get("due_before"):
        qs = qs.filter(due_date__lte=due_before)

    data = [
        {
            "title": t.title,
            "status": t.status,
            "priority": t.priority
        }
        for t in qs
    ]
    return JsonResponse(data, safe=False)


@login_required
# summary-view-anchor
def dashboard_view(request):
    projects_count = Project.objects.filter(owner=request.user).count()

    tasks_qs = Task.objects.filter(project__owner=request.user)

    total_tasks = tasks_qs.count()

    status_summary = (
        tasks_qs
        .values("status")
        .annotate(count=Count("id"))
    )

    upcoming_tasks = tasks_qs.filter(
        status__in=["todo", "in_progress"],
        due_date__isnull=False
    ).order_by("due_date")[:5]

    if not upcoming_tasks:
        upcoming = "No upcoming tasks!"
    else:
        upcoming = upcoming_tasks

    return render(
        request,
        "tracker/dashboard.html",
        {
            "projects_count": projects_count,
            "total_tasks": total_tasks,
            "status_summary": status_summary,
            "upcoming": upcoming,
        }
    )
