import datetime

from django.db import models
from django.utils import timezone
from django.core import serializers

""" states with fisheries | fisheries with crew | states with crew  
"""

class State(models.Model):
	# each state included in the db 
	state_name = models.CharField(max_length=30)
	state_nation = models.CharField(max_length=30)
	name_abbreviation = models.CharField(max_length=6)
	#fisheries
	#ports
	#crew
	#gigs
	
	def __str__(self):
		return name_abbreviation

class Fishery(models.Model):
	"""all relevant info for a specific fishery, changed from each state having 
	own table to each Fishery having a list of names? keys? to States where each
	Fishery is located"""
	fishery_name = models.CharField(max_length=50)
	#fishery_state = models.CharField(max_length=50)
	#fishery_state_id = models.ForeignKey(State, on_delete=models.CASCADE)
	"""rather than the two fields above, going with a "list" of ints
	representing the pk or ids of states where this fishery is located.
	according to django docs, CommaSeperatedIntegerField is deprecated now, so: """
	try:
		fishery_state_id_list = models.CharField(max_length=50, 
		validators=[validate_comma_seperated_integer_list])
	except(ValidationErr):
		return render(request, 'fgigs/addfishery.html', 
		{'fishery_name':fishery_name, 
		'error_message':"Fishery was not provided with comma seperated list of state.ids.",
			})
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
	last_updated = models.DateTimeField(auto_now=True, 'last updated on')
	
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
		
	serialized_data = serializers.serialize("json", Fishery.objects.all())
		
##########################################################################

class Crew(models.Model):
	""" crew can post to one fishery but in multiple states at once
	eg crew can post to Crab in Oregon, WA, CA all at same time (will travel)
	crew can only post to one fishery at a time or one port at a time and all fisheries
	crew can only post to home port
	crew can only post to one current port """
	crew_first_name = models.CharField(max_length=32)
	crew_last_name = models.CharField(max_length=32)
	
	#selected fishery this crew ad is for
	crew_fishery = models.ForeignKey(Fishery, on_delete=models.CASCADE)
	#date/time crew available to start work
	crew_available = models.DateTimeField
	#blurb crew ad poster can write about themselves
	crew_text = models.CharField(max_length=200)
	
	#port they live in or prefer to fish out of, "regular" port
	crew_home_port = models.CharField(max_length=32)
	#home_port_id = models.ForeignKey(Port, on_delete=models.CASCADE)
	home_port_state = models.CharField(max_length=32)
	home_port_state_id = models.ForeignKey(State, on_delete=models.CASCADE)
		
	#port they may be in currently, if different than home port
	crew_current_port = models.CharField(max_length=32)
	#current_port_id = models.ForeignKey(Port, on_delete=models.CASCADE)
	current_port_state = models.CharField(max_length=32)
	current_port_state_id = models.ForeignKey(State, on_delete=models.CASCADE)
	
	#years total of fishing experience
	fishery_exp_years = models.SmallIntegerField()
	
	#the time, date a user created a crew ad to post
	crew_ad_created = models.DateTimeField(auto_now_add=True)
	#the amount of time user selected their ad to run, in days eg: 3,5,7
	crew_ad_runtime = models.IntegerField()
	
	#fisheries crew has most experience in
	fishery_exp_1 = models.CharField(max_length=50)
	fishery_exp_2 = models.CharField(max_length=50)
	fishery_exp_3 = models.CharField(max_length=50)
	#brief summary of any other fishery experience
	fishery_exp_other = models.CharField(max_length=150)
	#whether crew is considered "green" or not
	#change this to a NullBooleanField() ?
	is_green = models.BooleanField()
	#any further description of their skills
	skills_desc = models.CharField(max_length=150)
	
	#whether crew will to another port for work or not
	will_travel = models.BooleanField()
	phone_number = models.CharField(max_length=30)
	email_addr = models.CharField(max_length=50)
	
	
	#how many views this crew's ad has gotten
	#crew_looks = models.IntegerField(default=0) #how many time someone has looked at their profile

	def __str__(self):
		#I guess the + is still the fastest/easiest concat method here?
		info_summary = "Crew info summary: " + crew_first_name + " " +
		crew_last_name + "/nFishery: " + crew_fishery + "/nAbout: " + crew_text + "/n"
		"Home port: " + crew_home_port + "Current port, if different: " +
		crew_current_port + "/nYears experience: " + fishery_exp_years + 
		"Experience in fisheries:/n" + fishery_exp_1 + " " + fishery_exp_2 +
		" " + fishery_exp_3 + " " + fishery_exp_other + "/nSkills: " +
		skills_desc + "/nWill travel: " + will_travel + "/nPhone" + phone_number +
		" Email: " + email_addr + "/nAvailable to start: " + crew_available
		return info_summary
		
	def crew_is_expired(self):
		#check to see if the ad should still be displayed or if it has expired
		#should return false if time difference is positive, true if negative
		current_time = timezone.now()
		#eg post on noon monday for 5 days, check at noon tuesday should still
		#be positive? right? def check this logic again
		return current_time - datetime.timedelta(days=self.crew_ad_runtime) <=
		self.crew_ad_created <= now
		
	serialized_data = serializers.serialize("json", Crew.objects.all())
