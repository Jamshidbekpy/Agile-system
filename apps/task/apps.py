from django.apps import AppConfig


class TaskConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.task"
    
    def ready(self):
        from . import translation # noqa
        import apps.task.signals # noqa
