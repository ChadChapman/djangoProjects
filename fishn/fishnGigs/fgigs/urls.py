from django.conf.urls import url

from . import views

urlpatterns = [
	# /fgigs/
	url(r'^$', views.index, name='index'),
	# /fgigs/5/
	url(r'^(?P<fishery_id>[0-9]+)/$', views.detail, name='detail'),
	# /fgigs/5/crew/
	url(r'^(?P<fishery_id>[0-9]+)/crew/$', views.crew, name='crew'),
	# /fgigs/5/vote/
	url(r'^(?P<fishery_id>[0-9]+)/vote/$', views.results, name='vote'),
	]

	################# tut part 3 start here
