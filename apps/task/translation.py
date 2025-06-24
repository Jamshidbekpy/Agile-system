from modeltranslation.translator import register, TranslationOptions

from .models import Task, TaskHistory

@register(Task)
class TaskTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

@register(TaskHistory)
class TaskHistoryTranslationOptions(TranslationOptions):
    fields = ('action',)