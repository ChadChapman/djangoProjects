import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Fishery

def create_fishery(description_text, days):
	""" new fishery with param description text and param days as for update
	delta, neg. days are in past and pos. days are in future. """
	time = timezone.now() + datetime.timedelta(days=days)
	return Question.objects.create(description_text=description_text,
	updated_date=updated_date)

# create tests below.
#to run in term: python3 manage.py test fgigs
#test method must begin with "test_..."

#####################################################################

#model tests
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

#####################################################################

#view tests
class QuestionIndexViewTests(TestCase):
	
	def test_no_fisheries(self):
		""" if no fisheries, display emptyList template """
		response = self.client

#####################################################################
#~ testing in the shell:
	#~ from django.text.utils import setup_test_environment
	#~ setup_test_environment()
	#~ from django.test import Client
	#~ client = Client()
	#~ # test '/'
	#~ response = client.get('/')
	#~ response.status_code
	#~ from django.urls import reverse
	#~ response = client.get(reverse('fgigs:index'))
	#~ response.status_code
	#~ response.content
	#~ response.context['latest_fishery_list']
