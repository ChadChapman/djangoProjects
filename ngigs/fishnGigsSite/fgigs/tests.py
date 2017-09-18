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
class FisheryIndexViewTests(TestCase):
	#some of these tests should be broken up into several tests
	def test_no_fisheries(self):
		""" if no fisheries, display emptyList template """
		response = self.client.get(reverse('fgigs:index'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "No fisheries are available.")
		self.assertQuerysetEqual(response.context['latest_question_list'], [])
		
	def test_past_fishery(self):
		"""Fisheries with updated_recently in the past are displayed on index page"""
		create_fishery(description_text="Past updated fishery.", days=-30)
		response = self.client.get(reverse('fgigs:index'))
		self.assertQuerysetEqual(response.context['latest_question_list'],
		['<Fishery: Past fishery.>'])
		
	def test_future_fishery(self):
		"""Fisheries with an update_date in the future aren't displayed on index page yet."""
		create_fishery(description_text="Future fishery.", days = 30)
		response = self.client.get(reverse'fgigs:index'))
		self.assertContains(response, "No fisheries are available.")
		self.assertQuerysetEqual(response.context['latest_fishery_list'],[])
		
	def test_future_fishery_and_past_fishery(self):
		"""If both past and future fisheries exist, only past are displayed"""
		create_fishery(description_text="Past fishery.", days=-30)
		create_fishery(description_text="Future fishery.", days=30)
		response = self.client.get(reverse('fgigs:index'))
		self.assertQuerysetEqual( response.context['latest_fishery_list'],
		['<Fishery: Past fishery.>'])
		
	def test_two_past_fisheries(self):
		"""Fishery index page can display >1 fisheries"""
		create_fishery(description_text="Past fishery 1.", days=-30)
		create_fishery(description_text="Past fishery 2.", days=-10)
		response = self.client.get(reverse('fgigs:index'))
		self.assertQuerysetEqual(response.context['latest_fishery_list'],
		['<Fishery: Past fishery 2.>', '<Fishery: Past fishery 1.>'])	

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
