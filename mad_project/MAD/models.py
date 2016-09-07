from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings

# This code is triggered whenever a new user has been created and saved to the database

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class UserProfile(models.Model):  
    user = models.OneToOneField(User, related_name='own')
    firstLogIn = models.BooleanField(default=True)
    
    def __unicode__(self):
        return self.user.username

#Activities table
class Activities(models.Model):
    name = models.CharField(max_length=128)
    venue = models.CharField(max_length=128)
    postcode = models.CharField(max_length=16, blank=True)
    agesLower = models.IntegerField(default=3)
    agesUpper = models.IntegerField(default=100)
    contactName = models.CharField(max_length=128, null=True, blank=True)
    contactEmail = models.EmailField(max_length=256, null=True, blank=True)
    number = models.CharField(max_length=32, blank=True)
    special = models.CharField(max_length=256, blank = True)
    owner = models.ForeignKey('auth.User', null=True)

    def __unicode__(self):      #For Python 2, use __str__ on Python 3
        return self.name


#Category table
class Categories(models.Model):
    name = models.CharField(max_length=128)
    
    def __unicode__(self):      #For Python 2, use __str__ on Python 3
        return self.name


#Activities and category junction table
class act_cat(models.Model):
    act = models.ForeignKey(Activities, null=True, related_name='cats')
    cat = models.ForeignKey(Categories, null=True)
   


#Activities and category junction table
class act_day(models.Model):
    act = models.ForeignKey(Activities, null=True, related_name='days')
    day = models.CharField(max_length=32)
    startTime = models.TimeField(null=False, blank=False, default='12:00')
    endTime = models.TimeField(null=False, blank=False, default='12:00')

