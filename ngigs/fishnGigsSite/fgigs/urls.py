
"""
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
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
	url(r'^$', views.IndexView.as_view(), name='index'),
	
	# /fgigs/fisheries/all/
	# show index of all fisheries, direct link from index page button
	url(r'^fisheries/all/$', views.FisheryAllIndexView.as_view(), name='fisheryallindex'),
	
	# /fgigs/fisheries/3/
	# show fishery with pk=3, all states included, states separated? by color or ?
	url(r'^fisheries/(?P<fishery_id>[0-9]+)/$', views.FisheryPKView.as_view(), name='fisherypk'),
	
	# /fgigs/fisheries/3/crew/
	# show crew ads for fishery where fishery pk=3
	url(r'^fisheries/(?P<fishery_ids>[0-9]+)/crew/$', views.FisheryPKCrewView.as_view(), name='fisherypkcrew'),
	
	# /fgigs/5/
	#url(r'^(?P<fishery_id>[0-9]+)/$', views.detail, name='detail'),
	#url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
	
	
			
	
	
	
		
	# /fgigs/fisheries/3/states/2/
	# show fishery with pk=3, in state with pk = 2
	url(r'^fisheries/(?P<fishery_id>[0-9]+)/states/(?P<state_id>[0-9]+)/$', views.FisheryPKStatePKView.as_view(), name='fisherypkindex'),
		
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

