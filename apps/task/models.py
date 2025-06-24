from django.db import models
from django.contrib.auth import get_user_model
from apps.common.models import BaseModel
from .choices import TaskStatus, TaskPriority
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class Task(BaseModel):
    title = models.CharField(_('Title'),max_length=255)
    description = models.TextField(_('Description'))

    assignee = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_tasks"
    )

    status = models.CharField(
        max_length=30,
        choices=TaskStatus.CHOICES,
        default=TaskStatus.BACKLOG
    )

    priority = models.CharField(
        max_length=10,
        choices=TaskPriority.CHOICES,
        default=TaskPriority.LOW
    )

    rejection_comment = models.TextField(blank=True, null=True)
    class Meta:
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')
        ordering = ['-priority', '-created_at']

    def is_high_priority(self):
        return self.priority == TaskPriority.HIGH

    def __str__(self):
        return f"{self.title} [{self.status}] ({self.priority})"

class TaskHistory(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="history")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.TextField(_('Action'))
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('Task History')
        verbose_name_plural = _('Task Histories')
        ordering = ['-timestamp']

    def __str__(self):
        return f"[{self.timestamp}] {self.user}: {self.action}"
