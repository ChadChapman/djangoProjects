import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Fishery

# Create your tests here.
#to run in term: python3 manage.py test fgigs
#test method must begin with "test..."
class FisheryModelTests(TestCase):
	
	def test_was_published_recently_with_future_fishery(self):
		""" was_updated_recently() returns False for fisheryies whose update
		date is in the future. """
		time = timezone.now() + datetime.timedelta(days=30)
		future_fishery = Fishery(pub_date = time)
		self.assertIs(future_fishery.was_updated_recently(), False)

	def test_was_updated_recently_with_old_info(self):
		""" was_updated_recently returns False for fisheries with update_date
		older than 1 day. """
		time = timezone.now() - datetime.timedelta(days=1, seconds =1)
		old_fishery = Fishery(update_date = time)
		self.assertIs(old_fishery.was_updated_recently(), False)
		
	def test_was_updated_recently_with_recent_fishery(self):
		""" was_updated_recently() returns True for fisheries with update_date
		is within last 24 hours. """
		time = timezone.now() - datetime.timedelta(hours=23, minutes=59, 
		seconds=59)
		recent_fishery = Fishery(update_date = time)
		self.assertIs(recent_fishery.was_updated_recently(),True)
