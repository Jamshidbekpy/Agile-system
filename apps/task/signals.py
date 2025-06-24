# apps/task/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from apps.task.models import Task, TaskHistory, TaskPriority
from apps.task.tasks import send_high_priority_email, enqueue_priority_task

@receiver(post_save, sender=Task)
def notify_on_high_priority_task(sender, instance, created, **kwargs):
    if instance.priority == TaskPriority.HIGH:
        message = f"Shoshilinch! #{instance.id}-vazifa (High): '{instance.title}'"

        # WebSocket orqali real vaqtli bildirishnoma
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "notifications",
            {
                "type": "send_notification",
                "message": message
            }
        )

        # Tarixga yozish
        if not created:
            TaskHistory.objects.create(
                task=instance,
                user=instance.assignee,
                action=f"Priority: {instance.priority.upper()} (High priority trigger)"
            )

        # Email yuborish Celery orqali
        send_high_priority_email.delay(task_id=instance.id)

        # Task’ni navbatga qo‘yish (priority queue)
        enqueue_priority_task.apply_async((instance.id,), priority=10)
