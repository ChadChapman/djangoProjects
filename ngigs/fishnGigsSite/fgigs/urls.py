from django.conf.urls import url

from . import views

app_name = 'fgigs'
urlpatterns = [
	# /fgigs/
	#url(r'^$', views.index, name='index'),
	url(r'^$', views.IndexView.as_view(), name='index'),
	
	# /fgigs/5/
	#url(r'^(?P<fishery_id>[0-9]+)/$', views.detail, name='detail'),
	#url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
	
	# /fgigs/fisheries/
	# show index of all fisheries
	url(r'^fisheries/$', views.FisheryIndexView.as_view(), name='fisheryindex'),
			
	# /fgigs/fisheries/3/
	# show fishery with pk=3
	
	# /fgigs/ports/3/crew/
	# show crew ads for fishery where fishery pk=3
	
	# /fgigs/fisheries/state/2/?
	# show fisheries in state where state has id or pk=2
	# need to make State model then? dive into this later
	
	####################################################################
	# /fgigs/5/crew/
	#url(r'^(?P<fishery_id>[0-9]+)/crew/$', views.crew, name='crew'),
	url(r'^(?P<fishery_id>[0-9]+)/crew/$', views.crew, name='crew'),
	
	# /fgigs/5/vote/
	#url(r'^(?P<fishery_id>[0-9]+)/vote/$', views.results, name='vote'),
	url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
	]

