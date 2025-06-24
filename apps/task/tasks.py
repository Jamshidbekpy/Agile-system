from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from apps.task.models import Task

User = get_user_model()

@shared_task
def send_high_priority_email(task_id):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return

    subject = f"[HIGH PRIORITY] Task #{task.id}: {task.title}"
    message = f"Shoshilinch! Ushbu vazifa yuqori ustuvorlikda: {task.title}\n\n{task.description}"
    
    recipients = User.objects.values_list("email", flat=True)
    send_mail(subject, message, "admin@agile.uz", recipients)


@shared_task(bind=True)
def enqueue_priority_task(self, task_id):
    try:
        task = Task.objects.get(id=task_id)
        # Bu yerda siz boshqa processlar bilan bog‘lashiz mumkin: masalan, Slack yuborish, Telegram bot, audit...
        print(f"Queued High Priority Task: {task.title}")
    except Task.DoesNotExist:
        self.retry(countdown=5, max_retries=3)
