import datetime

from django.db import models
from django.utils import timezone

# Create your models here.
#fisheries and crew in those fisheries to begin with

class Fishery(models.Model):
	#all relevant info for a specific fishery, in a specific state
	#eg Oregon Crab will be a different table than Washington Crab
	fishery_name = models.CharField(max_length=50)
	fishery_state = models.CharField(max_length=50)
	#seasons of year: Summer, Fall, Winter, Spring or any set out of those
	fishery_seasons = models.CharField(max_length=50)
	#brief description of specific fishery such as seine vs troll salmon
	fishery_description = models.CharField(max_length=100)
	#first offical day of fishery season, so w/o strikes or other delays
	#if several openers during the year, this will be the next opener date
	opening_date = models.DateTimeField('season start date')
	#any known required licenses for participating in this fishery
	#make sure to clearly note this is not official and no liability on site owner 
	fishery_licenses = models.CharField(max_length=150)
	#the field below is to keep track of when crew or jobs added to this fishery
	last_updated = models.DateTimeField('last updated on')
	
	#method to signal if this Fishery has been updated in the last n amount of time
	#currently n is 1 day 
	def was_updated_recently(self):
		now = timezone.now()
		return now - datetime.timedelta(days=1) <= self.updated_date <= now
		#return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
		was_updated_recently.admin_order_field = 'updated_date'
		was_updated_recently.boolean = True
		was_updated_recently.short_description = 'Updated recently?'
	
	#return the fishery name, state, seasons, description, seasons, 
	#opening, licenses and when updated?
	def __str__(self): #toString method
		info_summary = "About Fishery: " + fishery_name + " in " + fishery_state + 
		" Description: /n" + fishery_description + "/n" + "Next opening date: " +
		opening_date
		
		return info_summary
		
##########################################################################

class Crew(models.Model):
	#crew can post to one fishery but in multiple states at once
	#eg crew can post to Crab in Oregon, WA, CA all at same time (will travel)
	#crew can only post to one fishery at a time or one port at a time and all fisheries
	#crew can only post to home port
	#crew can only post to one current port
	
	#selected fishery this crew ad is for
	crew_fishery = models.ForeignKey(Fishery, on_delete=models.CASCADE)
	#blurb crew ad poster can write about themselves
	crew_text = models.CharField(max_length=200)
	
	#how many views this crew's ad has gotten
	#crew_looks = models.IntegerField(default=0) #how many time someone has looked at their profile

	def __str__(self):
		return self.crew_text
