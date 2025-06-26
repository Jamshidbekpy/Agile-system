from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_email_async(to_email, subject, message):
    send_mail(
        subject=subject,
        message=message,
        from_email="jamshidbekdev04@gmail.com",
        recipient_list=[to_email],
        fail_silently=False,
    )
