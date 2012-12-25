from django.db import models

class Character(models.Model):
    first_name = models.CharField(max_length=20,blank=True,null=True)
    middle_name = models.CharField(max_length=20,blank=True,null=True)
    last_name = models.CharField(max_length=30,blank=True,null=True)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=30)
    def __unicode__(self):
        return '{0} {1} {2}'.format(self.first_name,self.middle_name,self.last_name)

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
