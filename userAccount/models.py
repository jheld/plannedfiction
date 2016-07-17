from django.db import models
#from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
#from django.db.models.signals import post_save

class MyUserManager(BaseUserManager):
    def create_user(self, username, password,first_name,last_name):
        if not username:
            raise ValueError('Users must have a username')
        if not first_name:
            raise ValueError('Users must have a first name')
        if not last_name:
            raise ValueError('Users must have a last name')
        if not password:
            raise ValueError('Users must have a password')
        user = self.model(
            username = username,
            first_name = first_name,
            last_name = last_name,
            )

        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, username, password,first_name,last_name):
        user = self.create_user(username,password=password,first_name=first_name,last_name=last_name)
        user.is_admin = True
        user.save(using=self._db)
        return user

class MyUser(AbstractBaseUser):
    username = models.CharField(max_length=40,unique=True,db_index=True)
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=25)
    USERNAME_FIELD = 'username'
    date_of_birth = models.DateField(blank=True,null=True)
    REQUIRED_FIELDS = ['first_name','last_name']
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    objects = MyUserManager()
    def __unicode__(self):
        return self.username
    def get_full_name(self):
        return '{fName} {lName}'.format(fName=self.first_name,lName=self.last_name)
    def get_short_name(self):
        return self.first_name
    def has_perm(self, perm,obj=None):
        return True
    def has_module_perms(seelf, app_label):
        return True
    @property
    def is_staff(self):
        return self.is_admin

'''
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance)

post_save.connect(create_user_profile, sender=User)
'''
