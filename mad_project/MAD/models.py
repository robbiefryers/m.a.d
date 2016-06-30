from django.db import models
from django.contrib.auth.models import User
#Activities table
class Activities(models.Model):
    name = models.CharField(max_length=128)
    venue = models.CharField(max_length=128)
    postcode = models.CharField(max_length=16)
    agesLower = models.IntegerField(default=3)
    agesUpper = models.IntegerField(default=100)
    contactName = models.CharField(max_length=128, null=True)
    contactEmail = models.EmailField(max_length=256, null=True)
    number = models.IntegerField(null=True)
    special = models.CharField(max_length=256)
    owner = models.ForeignKey(User, null=True)

    def __unicode__(self):      #For Python 2, use __str__ on Python 3
        return self.name


#Category table
class Categories(models.Model):
	name = models.CharField(max_length=128)
	
	
	def __unicode__(self):      #For Python 2, use __str__ on Python 3
		return self.name


#Activities and category junction table
class act_cat(models.Model):
    act = models.ForeignKey(Activities, null=True)
    cat = models.ForeignKey(Categories, null=True)

#Activities and category junction table
class act_day(models.Model):
    act = models.ForeignKey(Activities, null=True)
    day = models.CharField(max_length=32)
    startTime = models.TimeField(null=False, blank=False, default='12:00')
    endTime = models.TimeField(null=False, blank=False, default='12:00')