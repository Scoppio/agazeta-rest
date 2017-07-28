import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    ACCOUNT_TYPE = (
        ('f', 'Free'),
        ('p', 'Paid'),
        ('d', 'Demo'),
        ('c', 'Consultant'),
        ('s', 'Staff')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_type = models.CharField(max_length=30, choices=ACCOUNT_TYPE, default=ACCOUNT_TYPE[0])
    avatar = models.UUIDField(default=uuid.uuid4, editable=False)
    partner_sub = models.BooleanField(default=True)
    newsletter_sub = models.BooleanField(default=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class TobToken(models.Model):
    SERVERS = (
        ('a', 'Americas'),
        ('e', 'Europa'),
        ('c', 'Asia'),
    )
    username = models.CharField(max_length=80)
    token = models.CharField(max_length=80)
    server = models.CharField(max_length=10, choices=SERVERS, default=SERVERS[0])
    is_active = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        unique_together = ['username', 'token']

    def __str__(self):
        return "tob_token [is_active={} server={}]".format(self.is_active, self.server)

    def __repr__(self):
        return "tob_token [id={} username={} is_active={} server={} {}]".format(self.id, self.username, self.is_active, self.server, self.user)
