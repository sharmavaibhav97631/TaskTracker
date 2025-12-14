from django.contrib import admin
from .models import Project, Task


class TaskInline(admin.TabularInline):
    model = Task
    extra = 0
    fields = (
        "title",
        "status",
        "priority",
        "due_date",
        "assignee",
    )
    ordering = ("priority", "due_date")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "owner",
        "created_at",
        "updated_at",
    )
    list_filter = ("owner", "created_at")
    search_fields = ("name", "description", "owner__username")
    ordering = ("-created_at",)
    inlines = [TaskInline]

    def get_queryset(self, request):
        """
        Optimize queries when showing projects with tasks
        """
        qs = super().get_queryset(request)
        return qs.select_related("owner")

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "project",
        "status",
        "priority",
        "due_date",
        "assignee",
        "created_at",
    )
    list_filter = (
        "status",
        "priority",
        "due_date",
        "project",
    )
    search_fields = (
        "title",
        "description",
        "project__name",
        "assignee__username",
    )
    ordering = ("priority", "due_date")

    def get_queryset(self, request):
        """
        Optimize admin queries
        """
        qs = super().get_queryset(request)
        return qs.select_related("project", "assignee", "project__owner")
