from django.shortcuts import render
from django.http import HttpResponse
from .models import Fishery
#from django.template import loader

# Create your views here.
def index(request):
	latest_fishery_list = Fishery.objects.order_by('-pub_date')[:5]
	template = loader.get_template('fgigs/index.html')
	context = {'latest_fishery_list': latest_fishery_list,}
	return render(request, 'fgigs/index.html', context)
	#return HttpResponse(template.render(context,request))
	#output = ','.join([f.description_text for f in latest_fishery_list])
	#return HttpResponse(output)
	#return HttpResponse("index page!")
	
def detail(request, fishery_id):
	#takes the place of the try/catch block below
	fishery = get_object_or_404(Fishery, pk=fishery_id)
	#also a get_list_or_404() - uses filter() and 404s if list empty
	return render(request, 'fgigs/detail.html', {'fishery':fishery})	
	#~ try:
		#~ fishery = Fishery.objects.get(pk=fishery_id)
	#~ except:
		#~ raise Http404("Fishery does not exist")
	#~ return render(request, 'fgigs/detail.html', {'question':question})
	#~ #return HttpResponse("this is fishery number %s." % fishery_id)

def results(request, fishery_id):
	response = "this is the result from fishery %s."
	return HttpResponse(response % fishery_id)

def crew(request, fishery_id):
	return HttpResponse("this is crew for fishery %s." % fishery_id)
