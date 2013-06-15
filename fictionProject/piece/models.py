from django.db import models
from django.conf import settings

from subject.models import Character
from event.models import Event

class Piece(models.Model):
    title = models.CharField(max_length=100,unique=True)
    events = models.ManyToManyField(Event,null=True,blank=True)
    characters = models.ManyToManyField(Character,null=True,blank=True)
    # The user who created the piece
    creators = models.ManyToManyField(settings.AUTH_USER_MODEL)
    '''
    # Times where people are collaborating, but may not be explicit owners; e.g., editor,reviewer,friend.
    collaborators = models.ManyToManyField(settings.AUTH_USER_MODEL,null=True,blank=True)
    # In case 2 > users have equal ownership on a piece; e.g. writing partners.
    equal_owners = models.ManyToManyField(settings.AUTH_USER_MODEL,null=True,blank=True)
    '''
    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return '/pieces/{id}/'.format(id=self.id)
