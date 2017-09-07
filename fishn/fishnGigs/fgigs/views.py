from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
	return HttpResponse("index page!")

def detail(request, fishery_id):
	return HttpResponse("this is fishery number %s." % fishery_id)

def results(request, fishery_id):
	response = "this is the result from fishery %s".
	return HttpResponse(response % fishery_id)

def crew(request, fishery_id):
	return HttpResponse("this is crew for fishery %s." % fishery_id)
