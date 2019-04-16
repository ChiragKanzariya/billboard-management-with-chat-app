from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User
from django.utils import timezone



@python_2_unicode_compatible
class Post(models.Model):
    owner = models.ForeignKey(User, related_name="billboard_owner", on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name="billboard_user", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    clip = models.FileField(upload_to='static/upload/', null=True)
    date_to = models.DateField(null=True)
    date_from = models.DateField(null=True)
    time_to = models.TimeField(null=True)
    time_from = models.TimeField(null=True)


class Invitation(models.Model):
    from_author = models.ForeignKey(
        User, 
        related_name="invitations_sent", 
        on_delete=models.CASCADE
        )
    to_owner = models.ForeignKey(
        User, 
        related_name="invitations_received",
        verbose_name="Owner to request",
        help_text="select owner to send request!", 
        on_delete=models.CASCADE
        )
    title = models.CharField(max_length=200)
    clip = models.FileField(upload_to='static/upload/', null=True)
    date_to = models.DateTimeField(null=True)
    date_from = models.DateTimeField(null=True)
    time_to = models.TimeField(null=True)
    time_from = models.TimeField(null=True)
    message = models.CharField(
        max_length=300, blank=True,
        verbose_name="Message",
        help_text="It's always nice to add specific detail here!"
        )
    timestamp = models.DateTimeField(auto_now_add=True)


   
