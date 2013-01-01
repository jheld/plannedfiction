from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    def __unicode__(self):
        return self.user.username

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance)

post_save.connect(create_user_profile, sender=User)

class Character(models.Model):
    name = models.CharField(max_length=60,blank=False,null=False)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=30)
    def __unicode__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    location = models.CharField(max_length=250,blank=True,null=True)
    time = models.DateTimeField(blank=True,null=True)
    characters = models.ManyToManyField(Character, null=True,blank=True)
    order = models.PositiveIntegerField(blank=True,null=True)
    def __unicode__(self):
        return self.name

class Piece(models.Model):
    title = models.CharField(max_length=100,unique=True)
    events = models.ManyToManyField(Event,null=True,blank=True)
    characters = models.ManyToManyField(Character,null=True,blank=True)
    def __unicode__(self):
        return self.title
