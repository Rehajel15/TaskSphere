from django.db.models.signals import post_save
from django.dispatch import receiver
from home.models import Table, Group


@receiver(post_save, sender=Group)
def create_profile(sender, instance, created, **kwargs):
    if created:
        new_table = Table.objects.create(group=instance)
        new_table.save()
        