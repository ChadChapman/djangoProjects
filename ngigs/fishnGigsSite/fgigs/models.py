import datetime

from django.db import models
from django.utils import timezone

# Create your models here.
#fisheries and crew in those ports to begin with

class Fishery(models.Model):
	description_text = models.CharField(max_length=200)
	opening_date = models.DateTimeField('season start date')
	updated_date = models.DateTimeField('last updated on')
	
	def was_updated_recently(self):
		now = timezone.now()
		return now - datetime.timedelta(days=1) <= self.updated_date <= now
		#return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

	def __str__(self): #toString method
		return self.description_text


##########################################################################

class Crew(models.Model):
	crew_fishery = models.ForeignKey(Fishery, on_delete=models.CASCADE)
	crew_text = models.CharField(max_length=200)
	crew_looks = models.IntegerField(default=0) #how many time someone has looked at their profile

	def __str__(self):
		return self.crew_text
