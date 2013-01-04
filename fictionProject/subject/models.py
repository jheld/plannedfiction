from django.db import models

# Create your models here.
class Character(models.Model):
    name = models.CharField(max_length=60,blank=False,null=False)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=30)
    height = models.PositiveIntegerField(blank=True,null=True)
    eye_color = models.CharField(max_length=15,blank=True,null=True)
    race = models.CharField(max_length=25,blank=True,null=True)
    def __unicode__(self):
        return self.name