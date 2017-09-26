
"""
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views - !not used!
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views - !is used!
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url

from . import views

app_name = 'fgigs'
urlpatterns = [
	#leading slash is implied and does not have to be added in urls
	# /fgigs/
	#url(r'^$', views.index, name='index'),
	url(r'^$', views.IndexView.as_view(), name='index')
	
	##################################################################
	""" fishery routings
	"""
	######################### META FISHERIES ###########################
	
	# /fgigs/fisheries/all/
	# show index of all meta fisheries, direct link from index page button
	url(r'^fisheries/all/$', views.FisheryAllIndexView.as_view(), name='fisheryallindex')
	
	# /fgigs/fisheries/3/details/
	# metafishery, with details. eg Salmon, Crab, Tuna
	url(r'^fisheries/(?P<metafishery_id>[0-9]+)/details/$', views.MetaFisheryDetailView.as_view(), name='fisherydetail')
		
	# /fgigs/fisheries/3/states/
	# show all states for metafishery type where metafishery type = 3
	url(r'^fisheries/(?P<metafishery_id>[0-9]+)/states/$', views.MetaFisheryAllStatesView.as_view(), 
	name='metafisheryallstates')
	
	# /fgigs/fisheries/3/crew/
	# show crew ads for metafishery where metafishery pk=3
	url(r'^fisheries/(?P<metafishery_id>[0-9]+)/crew/$', views.MetaFisheryAllCrewView.as_view(), 
	name='metafisheryallcrew')
	
	##################### FISHERIES BY STATE ###########################
	 
	# /fgigs/fisheries/3/states/2/details
	# show fishery with pk=3, in a specific state with state pk = 2, view is a DetailView
	url(r'^fisheries/(?P<type_id>[0-9]+)/states/(?P<state_id>[0-9]+)/$', 
	views.FisheryStateDetailView.as_view(), name='fisherystatedetail')
	
	# /fgigs/fisheries/3/states/2/crew/
	# show fishery with pk=3, in state with pk = 2
	url(r'^fisheries/(?P<fishery_id>[0-9]+)/states/(?P<state_id>[0-9]+)/crew/$', 
	views.FisheryStateAllCrewView.as_view(), name='fisherystateallcrew'),
		
	####################################################################
	""" state routings
	"""
	####################################################################
	
	# /fgigs/states/all/
	# show index of all states, direct link from index page button
	url(r'^states/all/$', views.StateAllIndexView.as_view(), name='stateallindex')
	
	# /fgigs/states/3/details
	# detail view for specific state, show state with pk = 3
	url(r'^states/(?P<state_id>[0-9]+)/$', views.StateDetailView.as_view(), name='statedetail')
	
	# /fgigs/states/3/crew/
	# show crew ads for all fisheries in state where state pk = 3, 
	url(r'^states/(?P<state_id>[0-9]+)/crew/$', views.StateAllCrewView.as_view(), name='stateallcrew')
	
	# /fgigs/states/3/fisheries/
	# show all fisheries in state with state pk=3, 
	url(r'^states/(?P<state_id>[0-9]+)/fisheries/$', 
	views.StateAllFisheryView.as_view(), name='stateallfishery')
	
	##################################################################
	""" crew routings
	"""
	##################################################################
	
	# /fgigs/crew/all/  all crew listings, expired and active (admin only)
	url(r'^crew/all/$',	views.CrewAllIndexView.as_view(), name='crewallindex')
	
	# /fgigs/crew/new/  make new crew listing
	url(r'^crew/new/$',	views.CrewNewView.as_view(), name='crewnew')
	
	# /fgigs/crew/active/ see all live crew listings
	url(r'^crew/active/$', views.CrewActiveIndexView.as_view(), name='crewactiveindex')
	
	# /fgigs/crew/search/fishery/2/  look for crew in metafishery pk = 2
	url(r'^crew/search/fishery/(?P<metafishery_id>[0-9]+)/$', views.CrewMetaFisheryAllView.as_view(),
	 name='crewmetafisheryall')
	
	# /fgigs/crew/search/state/4/ look for crew in state pk = 4
	url(r'^crew/search/state/(?P<state_id>[0-9]+)/$', views.CrewStateIndexView.as_view(),
	 name='crewstateindex')
	
	# /fgigs/crew/search/state/4/fishery/3/ look for crew in state pk = 4, metafishery pk = 3
	#pretty redundant just need a redirect?
	
	##################################################################
	# /fgigs/5/
	#url(r'^(?P<fishery_id>[0-9]+)/$', views.detail, name='detail'),
	#url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
		
	# /fgigs/fisheries/state/2/?
	# show fisheries in state where state has id or pk=2
	# need to make State model then? dive into this later
	#url(r'^fisheries/wa/$', views.FisheryWAIndexView.as_view(), name='fisherywaindex'),
	#url(r'^fisheries/or/$', views.FisheryORIndexView.as_view(), name='fisheryorindex'),
	#url(r'^fisheries/ca/$', views.FisheryCAIndexView.as_view(), name='fisherycaindex'),
	#url(r'^fisheries/ak/$', views.FisheryAKIndexView.as_view(), name='fisheryakindex'),
	# url(r'^fisheries/hi/$', views.FisheryHIIndexView.as_view(), name='fisheryhiindex'),
	
	####################################################################
	# /fgigs/5/crew/
	#url(r'^(?P<fishery_id>[0-9]+)/crew/$', views.crew, name='crew'),
	url(r'^(?P<fishery_id>[0-9]+)/crew/$', views.crew, name='crew'),
	
	# /fgigs/5/vote/
	#url(r'^(?P<fishery_id>[0-9]+)/vote/$', views.results, name='vote'),
	url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
	]

