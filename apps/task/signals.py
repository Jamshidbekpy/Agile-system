from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext as _
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from apps.task.models import Task, TaskPriority, TaskStatus, TaskAssignee
from apps.task.tasks import send_email_async


def send_ws_and_email(user, subject, message, group_name=None):
    
    # Email orqali
    send_email_async.delay(user.email, subject, message)

    # WebSocket orqali
    group = group_name or f"notifications_{user.role}"
    async_to_sync(get_channel_layer().group_send)(
        group,
        {
            "type": "send_notification",
            "message": message
        }
    )


@receiver(post_save, sender=Task)
def handle_task_events(sender, instance, created, **kwargs):
    task_id = instance.id
    title = instance.title
    status = instance.status
    priority = instance.priority
    rejection_comment = instance.rejection_comment or _("No reason provided")
    assignees = [
        ta.assignee for ta in TaskAssignee.objects.select_related("assignee").filter(task=instance)
    ]

    # 1. Yangi vazifa → Project Manager
    if created:
        for user in assignees:
            if user.role == "project_manager":
                subject = _("New Task Assigned")
                message = _("New task created: '{}'").format(title)
                send_ws_and_email(user, subject, message, "notifications_project_manager")

    # 2. TO_DO status → Developer/Tester
    elif status == TaskStatus.TO_DO:
        for user in assignees:
            if user.role in ["developer", "tester"]:
                subject = _("Task Assigned")
                message = _("A task has been assigned to you: '{}'").format(title)
                send_ws_and_email(user, subject, message)

    # 3. IN_PROGRESS → Project Manager
    elif status == TaskStatus.IN_PROGRESS:
        developer = next((u for u in assignees if u.role == "developer"), None)
        developer_name = developer.username if developer else _("Unknown")
        for user in assignees:
            if user.role == "project_manager":
                subject = _("Task in Progress")
                message = _("#{id} task is in progress (Developer: {dev})").format(
                    id=task_id, dev=developer_name
                )
                send_ws_and_email(user, subject, message, "notifications_project_manager")

    # 4. READY_FOR_TESTING → Tester
    elif status == TaskStatus.READY_FOR_TESTING:
        for user in assignees:
            if user.role == "tester":
                subject = _("Task Ready for Testing")
                message = _("#{id} is ready for testing").format(id=task_id)
                send_ws_and_email(user, subject, message, "notifications_tester")

    # 5. REJECTED → Developer
    elif status == TaskStatus.REJECTED:
        for user in assignees:
            if user.role == "developer":
                subject = _("Task Rejected")
                message = _("#{id} was rejected: '{}'").format(task_id, rejection_comment)
                send_ws_and_email(user, subject, message, "notifications_developer")

    # 6. HIGH Priority → All Assignees
    if priority == TaskPriority.HIGH:
        for user in assignees:
            subject = _("Urgent Task!")
            message = _("URGENT! Task #{id} (High): '{title}'").format(id=task_id, title=title)
            send_ws_and_email(user, subject, message)

