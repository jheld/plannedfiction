from django.db import models

from subject.models import Character
from event.models import Event


class Piece(models.Model):
    title = models.CharField(max_length=100,unique=True)
    events = models.ManyToManyField(Event,null=True,blank=True)
    characters = models.ManyToManyField(Character,null=True,blank=True)
    def __unicode__(self):
        return self.title
