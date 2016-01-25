from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from models import ModelsChangesLog


@receiver(post_save)
def post_save_action(sender, created, **kwargs):
    model_name = sender.__name__
    if model_name == 'ModelsChangesLog':
        return
    action = 'create' if created else 'edit'
    ModelsChangesLog.objects.create(model_name=model_name, action=action)


@receiver(post_delete)
def post_delete_action(sender, **kwargs):
    model_name = sender.__name__
    if model_name == 'ModelsChangesLog':
        return
    ModelsChangesLog.objects.create(model_name=model_name, action='delete')
