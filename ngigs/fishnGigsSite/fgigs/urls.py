from django.conf.urls import url

from . import views

app_name = 'fgigs'
urlpatterns = [
	# /fgigs/
	#url(r'^$', views.index, name='index'),
	url(r'^$', views.IndexView.as_view(), name='index'),
	
	# /fgigs/5/
	#url(r'^(?P<fishery_id>[0-9]+)/$', views.detail, name='detail'),
	url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
	
	# /fgigs/5/crew/
	#url(r'^(?P<fishery_id>[0-9]+)/crew/$', views.crew, name='crew'),
	url(r'^(?P<fishery_id>[0-9]+)/crew/$', views.crew, name='crew'),
	
	# /fgigs/5/vote/
	#url(r'^(?P<fishery_id>[0-9]+)/vote/$', views.results, name='vote'),
	url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
	]

	################# tut part 3 start here
