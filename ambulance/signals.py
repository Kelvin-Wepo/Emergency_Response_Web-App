from django.db.models.signals import post_save
#post_save is the signal that is sent at the end of the save method.
from django.contrib.auth.models import User
from django.dispatch import receiver
# # importing the user profile model
from .models import Profile
from django.core.exceptions import ObjectDoesNotExist


@receiver(post_save, sender=User)
# def create_profile(sender, instance, created, **kwargs):    
def create_profile(sender, instance, created, *args, **kwargs):
# ignore if this is an existing User
    if not created:
        return
    Profile.objects.create(user=instance)
post_save.connect(create_profile, sender=User)
    
        
# # A profile is created every time a user is created
# #User is the sender which is responsible for making the notification.


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
    
    