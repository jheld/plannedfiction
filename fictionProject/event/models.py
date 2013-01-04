from django.db import models

from subject.models import Character

# Create your models here.
class Event(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    location = models.CharField(max_length=250,blank=True,null=True)
    time = models.DateTimeField(blank=True,null=True)
    characters = models.ManyToManyField(Character, null=True,blank=True)
    order = models.PositiveIntegerField(blank=True,null=True)
    def __unicode__(self):
        return self.name