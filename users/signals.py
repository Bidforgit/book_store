from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.contrib import messages
from django.contrib.auth.signals import user_logged_in, user_logged_out

from .models import Profile


def logged_in_message(sender, user, request, **kwargs):
    messages.info(
        request, f"Добро пожаловать {request.user}, вы вошли в систему и теперь можете арендовать, просматривать и оценивать книги. ")


def logout_message(sender, user, request, **kwargs):
    messages.info(
        request, f"Вы вышли из системы, увидимся позже {request.user}")


user_logged_out.connect(logout_message)
user_logged_in.connect(logged_in_message)


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    instance.profile.save()
