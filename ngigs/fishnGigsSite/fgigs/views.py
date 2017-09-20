from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Fishery, Crew
from django.urls import reverse
from django.views import generic
#from django.template import loader
from django.utils import timezone

# Create your views here.
#switched to class based generic views now
#ListView = display a list of objects
class IndexView(generic.ListView):
	#generic.ListView defaults to 'appName/modelName_list.html'
	#this overrides the default
	template_name = 'fgigs/index.html'
	#generic view autogens context var: fishery_list
	#overrides default, but could change template instead
	context_object_name = 'latest_fishery_list'
	#i think this actual index should just be the search by port or by fishery
	#landing page, with buttons for create a new ad for either
	def get_queryset(self):
		#return last five updated (published) fisheries
		return Fishery.objects.filter(updated_date__lte=
		timezone.now()).order_by('-pub_date')[:5]
		#return Fishery.objects.order_by('-pub_date')[:5]
		
#~ def index(request):
	#~ latest_fishery_list = Fishery.objects.order_by('-pub_date')[:5]
	#~ template = loader.get_template('fgigs/index.html')
	#~ context = {'latest_fishery_list': latest_fishery_list,}
	#~ return render(request, 'fgigs/index.html', context)
	#return HttpResponse(template.render(context,request))
	#output = ','.join([f.description_text for f in latest_fishery_list])
	#return HttpResponse(output)
	#return HttpResponse("index page!")
	
#################################################################

class FisheryIndexView(generic.ListView):
	#override the default template name
	template_name = 'fgigs/fisheryindex.html'
	#override the autogen context var with this:
	context_object_name = 'db_fishery_list'
	
	def get_queryset(self):
		#should return all fisheries in db
		return Fishery.objects.all()

#generic.DetailView = display page of details of one object
#generic.DetailView expects primary key as pk from URL
#generic.DetailView defaults to 'appName/modelName_detail.html for template	
class DetailView(generic.DetailView):
	model = Fishery
	#overriding the default template name, as mentioned above
	template_name = 'fgigs/detail.html'
	
	df get_queryset(self):
		"""Exclude fisheries with only future updates set."""
		return Fishery.objects.filter(updated_date__lte=timezone.now())
		
#~ def detail(request, fishery_id):
	#~ #takes the place of the try/catch block below
	#~ fishery = get_object_or_404(Fishery, pk=fishery_id)
	#~ #also a get_list_or_404() - uses filter() and 404s if list empty
	#~ return render(request, 'fgigs/detail.html', {'fishery':fishery})	
	#~ try:
		#~ fishery = Fishery.objects.get(pk=fishery_id)
	#~ except:
		#~ raise Http404("Fishery does not exist")
	#~ return render(request, 'fgigs/detail.html', {'question':question})
	#~ #return HttpResponse("this is fishery number %s." % fishery_id)

class ResultsView(generic.DetailView):
	model = Fishery
	#still a generic.DetailView but displaying as different template
	template_name = 'fgigs/results.html'
	
#~ def results(request, fishery_id):
	#~ fishery = get_object_or_404(Fishery, pk=fishery_id)
	#~ return render(request, 'fgigs/results.html', {'fishery':fishery})	

def crew(request, fishery_id):
	return HttpResponse("this is crew for fishery %s." % fishery_id)
	
def goget(request, fishery_id):
	fishery = get_object_or_404(Fishery, pk=fishery_id)
	try:
		selected_crew = fishery.crew_set.get(pk=request.POST['crew'])
	except(KeyError, Crew.DoesNotExist):
		#go back to selection form
		return render(request, 'fgigs/detail.html', {'fishery':fishery,
			'error_message':"Crew was not selected.",
			})
	else:
		selected_crew.votes +=1
		selected_crew.save()
		#return HttpResponseRedirect after successful POST, prevent
		#double posting if user hits Back btn
		return HttpResponseRedirect(reverse('fgigs:results',
		args = (fishery.id,)))
	
	#response = "this is the result from fishery %s."
	#return HttpResponse(response % fishery_id)	
