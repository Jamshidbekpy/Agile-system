from django.contrib import admin
from django.db.models import Case, When, Value, IntegerField
from django.utils.translation import gettext_lazy as _
from .models import Task, TaskHistory, TaskAssignee, Group, Notification


class TaskHistoryInline(admin.TabularInline):
    model = TaskHistory
    extra = 0
    readonly_fields = ("user", "action", "timestamp")
    can_delete = False
    verbose_name = _("Task History")
    verbose_name_plural = _("Task History")


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "status",
        "colored_priority",
        "created_at",
        "updated_at",
    )
    list_filter = ("status", "priority")
    search_fields = ("title", "description")
    readonly_fields = ("created_at", "updated_at")
    inlines = [TaskHistoryInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.annotate(
            priority_order=Case(
                When(priority="high", then=Value(1)),
                When(priority="medium", then=Value(2)),
                When(priority="low", then=Value(3)),
                default=Value(0),
                output_field=IntegerField(),
            )
        )
        return qs.order_by("-priority_order", "-created_at")

    def colored_priority(self, obj):
        color = {"low": "green", "medium": "orange", "high": "red"}.get(
            obj.priority, "gray"
        )
        from django.utils.html import format_html

        return format_html(
            '<span style="color: white; background-color: {}; padding: 3px 8px; border-radius: 6px;">{}</span>',
            color,
            obj.get_priority_display(),
        )

    colored_priority.short_description = "Priority"
    colored_priority.admin_order_field = "priority_order"


@admin.register(TaskHistory)
class TaskHistoryAdmin(admin.ModelAdmin):
    list_display = ("task", "user", "action", "timestamp")
    list_filter = ("timestamp", "user")
    search_fields = ("task__title", "action", "user__username")
    readonly_fields = ("task", "user", "action", "timestamp")
    ordering = ("-timestamp",)


@admin.register(TaskAssignee)
class TaskAssigneeAdmin(admin.ModelAdmin):
    list_display = ("task", "assignee")
    list_filter = ("task", "assignee")
    search_fields = ("task__title", "assignee__username")


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("group", "message", "timestamp")
    list_filter = ("group", "timestamp")
    search_fields = ("group__name", "message")
    readonly_fields = ("group", "message", "timestamp")
