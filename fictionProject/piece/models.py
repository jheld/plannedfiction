from django.db import models

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
