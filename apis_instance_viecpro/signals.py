from django.contrib.auth.models import Group
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver


@receiver(user_logged_in)
def add_to_group(sender, user, request, **kwargs):
    g1, _ = Group.objects.get_or_create(name="editors")
    g1.user_set.add(user)
