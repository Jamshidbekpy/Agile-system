from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.translation import gettext as _
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from .models import Task, TaskPriority, TaskStatus, TaskAssignee, Group, Notification
from .tasks import send_email_async


def send_ws_and_email(user, subject, message, group_name):
    # Email orqali
    send_email_async.delay(user.email, subject, message)

    # WebSocket orqali
    async_to_sync(get_channel_layer().group_send)(
        group_name,
        {
            "type": "send_notification",
            "message": f"{message} for {user.username}",
        },
    )
    group = Group.objects.get(name=group_name)
    Notification.objects.create(group=group, message=message)

# 1. Backlog → To Do Developer/Tester
@receiver(pre_save, sender=Task)
def handle_task_status_change(sender, instance, **kwargs):
    if not instance.pk:
        return  

    try:
        old_instance = Task.objects.get(pk=instance.pk)
    except Task.DoesNotExist:
        return  

    old_status = old_instance.status
    new_status = instance.status

    if old_status == TaskStatus.BACKLOG and new_status == TaskStatus.TO_DO:
        title = instance.title
        creator = instance.creator
        task_id = instance.pk

        assignees = [
            ta.assignee
            for ta in TaskAssignee.objects.select_related("assignee").filter(task=instance)
        ]

        for user in assignees:
            if user.role in ["developer", "tester"]:
                subject = _("Task Assigned")
                message = _(f"A task has been assigned to you: '{title}'")
                group_name = f"notifications_{creator.username}_{task_id}"
                send_ws_and_email(user, subject, message, group_name)       
                              
@receiver(post_save, sender=Task)
def handle_task_events(sender, instance, created, **kwargs):
    task_id = instance.id
    creator = instance.creator
    title = instance.title
    status = instance.status
    priority = instance.priority
    rejection_comment = instance.rejection_comment or _("No reason provided")
    assignees = [
        ta.assignee
        for ta in TaskAssignee.objects.select_related("assignee").filter(task=instance)
    ]

    # 2. Yangi vazifa → Project Owner
    if created:
        if creator.role == "project_owner":
            subject = _("New Task Assigned")
            message = _("New task created: '{}'").format(title)
            Group.objects.create(name=f"notifications_{creator.username}_{task_id}")
            group_name = f"notifications_{creator.username}_{task_id}"
            send_ws_and_email(creator, subject, message, group_name)
    



    # 3. IN_PROGRESS → Project Manager
    elif status == TaskStatus.IN_PROGRESS:
        developer = next((u for u in assignees if u.role == "developer"), None)
        developer_name = developer.username if developer else _("Unknown")
        for user in assignees:
            if user.role == "project_manager":
                subject = _("Task in Progress")
                message = _(f"{title} task is in progress (Developer: {developer_name})")
                group_name = f"notifications_{creator.username}_{task_id}"
                send_ws_and_email(user, subject, message, group_name)

    # 4. READY_FOR_TESTING → Tester
    elif status == TaskStatus.READY_FOR_TESTING:
        for user in assignees:
            if user.role == "tester":
                subject = _("Task Ready for Testing")
                message = _(f"{title} is ready for testing")
                group_name = f"notifications_{creator.username}_{task_id}"
                send_ws_and_email(user, subject, message, group_name)
    
    # 5. REJECTED → Developer
    elif status == TaskStatus.REJECTED:
        print("Rejected ##############################")
        for user in assignees:
            if user.role == "developer":
                subject = _("Task Rejected")
                message = _(f"#{title} was rejected: '{rejection_comment}'")
                print(message)
                group_name = f"notifications_{creator.username}_{task_id}"
                send_ws_and_email(user, subject, message, group_name)
        status = TaskStatus.TO_DO
        instance.status = status
        instance.save()

    # 6. HIGH Priority → All Assignees
    if priority == TaskPriority.HIGH:
        for user in assignees:
            subject = _("Urgent Task!")
            message = _(f"URGENT! Task #{task_id} (High): '{title}'")
            group_name = f"notifications_{creator.username}_{task_id}"
            send_ws_and_email(user, subject, message, group_name)
