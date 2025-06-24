from django.utils.translation import gettext_lazy as _

class TaskStatus:
    BACKLOG = 'backlog'
    TO_DO = 'to_do'
    IN_PROGRESS = 'in_progress'
    READY_FOR_TESTING = 'ready_for_testing'
    DONE = 'done'
    REJECTED = 'rejected'

    CHOICES = [
        (BACKLOG, _('Backlog')),
        (TO_DO, _('To Do')),
        (IN_PROGRESS, _('In Progress')),
        (READY_FOR_TESTING, _('Ready for Testing')),
        (DONE, _('Done')),
        (REJECTED, _('Rejected')),
    ]

class TaskPriority:
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'

    CHOICES = [
        (LOW, _('Low')),
        (MEDIUM, _('Medium')),
        (HIGH, _('High')),
    ]
