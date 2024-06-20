from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from .models import CustomUser
from .utils import assign_task_to_verifier

@receiver(user_logged_in)
def set_user_available(sender, user, request, **kwargs):
    # Set the user as available
    user.is_available = True
    user.save()

    # Call the function to assign tasks
    # assign_task_to_verifier()


@receiver(user_logged_out)
def set_user_unavailable(sender, user, request, **kwargs):
    # Set the user as available
    user.is_available = False
    user.save()
