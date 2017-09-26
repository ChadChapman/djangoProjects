from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Fishery, Crew
from django.urls import reverse
from django.views import generic
#from django.template import loader
from django.utils import timezone

# this is the class-based-views way of doing it, with generic views
#################################################################
"""
general index or landing page of the site, currently should offer to see
Crew by state, fishery, or both
+ button for add new Crew
+ button for add new Fishery (admin only)
+ button for add new State (admin only)
? not sure about detail views for state and fishery? buttons? 
"""
class IndexView(generic.ListView):
	#generic.ListView defaults to 'appName/modelName_list.html'
	#this overrides the default
	template_name = 'fgigs/index.html'
	#generic view autogens context var: fishery_list
	#overrides default, but could change template instead
	# ? context_object_name = 'latest_fishery_list' ?
	"""i think index page should just be: btn-search by state, btn-or by fishery,
	with buttons for create a crew ad for either state or fishery
	no querysets needed? template should just have buttons and nothing more needed here?
	"""	
	
""" ListView = display a list of objects.
there may be some overlap with displaying states, fisheries and ports when ports are added
i am leaving redundancy for now for ease of debugging and simplified logic
"""
#################################################################
# Fishery views: all fisheries in db, 
#				all fisheries in a state,
#				all fisheries with crew?
#				all crew for specific fishery in a specific state
#				individual fishery details,
#?
#################################################################

class FisheryAllIndexView(generic.ListView):
	""" all meta fisheries types in all states, state specific is handled below
	these should be by type_id and  
	"""
	#override the default template name
	template_name = 'fgigs/metafisheryallindex.html'
	#override the autogen context var with this:
	context_object_name = 'metafishery_all_list'
	
	def get_queryset(self):
		# should return all fisheries in db, it should be meta types, 
		# eg Salmon, Tuna, Crab and not state specific
		return MetaFishery.objects.all()
	
#################################################################

class MetaFisheryDetailView(generic.DetailView):
	""" one fishery, in all states 
	"""
	model = MetaFishery
	template_name = 'fgigs/metafisherydetail.html'
	context_object_name = 'metafishery_detail' 
	
	def get_queryset(self):
		try:
			metafishery_query = MetaFishery.objects.filter(id=metafishery_id)
		except(KeyError, MetaFishery.DoesNotExist, EmptyResultSet):
			return render(request, 'fgigs/metafisherynotfound.html', {
				'error_message':"No details for that Fishery were found.",
				})
		else:
			return metafishery_query
		
#################################################################

class MetaFisheryAllStatesView(generic.ListView):
	""" all states in a single metafishery. """
	template_name = 'fgigs/metafisheryallstates.html'
	context_object_name = 'metafishery_all_states_list' 
	""" each fishery has its own state, so get all fisheries with the fishery_id,
	then get the states out of those fisheries. This is just listing the states so no
	need to return actual State objects, names should be fine? then link names to btns
	on the template for each state's details? or state fishery details?
	"""
	def get_queryset(self):
		try:
			fishery_set = Fishery.objects.filter(fishery_type_id=_id)
		except(KeyError, Fishery.DoesNotExist, EmptyResultSet):
			return render(request, 'fgigs/fisherystatesnotfound.html', {
				'error_message':"No States were found for that Fishery.",
				})
		else:
			return fishery_set
	
	def get_state_list(request, type_id):
		""" here get the State names out of the metafisheries returned from the queryset.
		iterate through queryset and add State names to list
		"""
		query_return = self.get_queryset(self)
		#now make a list from queryset with a split() on the commas
		states_list = query_return.fishery_states.split(",")
		return state_list
	
#################################################################

class MetaFisheryAllCrewView(generic.ListView):
	""" all crew in a single metafishery. """
	template_name = 'fgigs/metafisheryallcrew.html'
	context_object_name = 'metafishery_all_crew_list' 
	
	def get_queryset(self):
		try:
			crew_set = Crew.objects.filter(crew_fishery_type_id=metafishery_id)
		except(KeyError, Fishery.DoesNotExist, EmptyResultSet):
			return render(request, 'fgigs/metafisherycrewnotfound.html', {
				'error_message':"No Crew were found for that Fishery.",
				})
		else:
			return crew_set
			
#################################################################

class FisheryStateDetailView(generic.DetailView):
	""" one fishery, in one state, both by pk or ids.  type_id for fishery and state_id
	should both be captured from url. DetailView because no list to display a this time. 
	"""
	model = Fishery
	template_name = 'fgigs/fisherystatedetail.html'
	context_object_name = 'fishery_state_detail' 
	
	def get_queryset(self):
		try:
			fishery_query = Fishery.objects.filter(fishery_type_id=type_id, fishery_state_id=state_id)
		except(KeyError, Fishery.DoesNotExist, EmptyResultSet):
			return render(request, 'fgigs/fisherystatedetailnotfound.html', {
				'error_message':"No details for this Fishery in this State were found.",
				})
		else:
			return fishery_query
	#aren't these two methods (above and below) doing basically the same thing?		
	def get_fishery_state_detail(request, type_id, state_id):
		fishery_state_obj = get_object_or_404(Fishery, fishery_type_id=type_id, 
		fishery_state_id=state_id)
		return render(request, 'fgigs/fisherystatedetail.html', 
		{'fishery_state_obj':fishery_state_obj})	 

########################################################################

class FisheryStateCrewView(generic.ListView):
	"""all crew listings for one fishery, in one state, 
	filtered by Fishery primary key (self.id) 
	"""
	template_name = 'fgigs/fisherystateallcrew.html'
	context_object_name = 'fishery_state_all_crew_list'
	
	def get_queryset(self):
		""" should return all crew listings for state-specific fishery
		Primary Key should be 'crew_fishery' """
		try:
			""" get queryset for pk if possible, 
			if not redirect to no crew in that fishery found page 
			"""
			crew_query = Crew.objects.filter(crew_fishery=fishery_id)
		except(KeyError, Crew.DoesNotExist, EmptyResultSet):
			return render(request, 'fgigs/fisherycrewnotfound.html', {
				'error_message':"Crew in that Fishery was not found.",
				})
		else:
			""" so the try worked, now make sure the template has the queryset and 
			renders it correctly.  
			"""
			return crew_query 
	
########################################################################

########################################################################
# State views: 	all states in db, 
#				all states in each fishery,
#				individual state details,
#? all states for each crew?
########################################################################
 
class StateAllIndexView(generic.ListView):
	""" all states found in the db
	"""
	template_name = 'stateallindex.html'
	context_object_name = 'state_all_list'
	
	def get_queryset(self):
		try:
			index_query = State.objects.all() 
		except (EmptyResultSet):
			return render(request, 'fgigs/statesnotfound.html', {
				'error_message':"All States were not found.",
				})
		else:
			return index_query 
	#queryset is iterable so think below method may be redundant		
	def get_state_list(self):
		state_query_all = self.get_queryset
		return list(state_query_all)	

#################################################################

class StateDetailView(generic.DetailView):
	""" detailed view of a state 
	"""
	model = State
	template_name = 'statedetail.html'
	
	def get_queryset(self):
		try:
			state_query = State.objects.filter(id = state_id)
		except(KeyError, State.DoesNotExist, ExptyResultSet):
			 return render(request, 'fgigs/statedetailnotfound.html', {
				'error_message':"The details for that State were not found.",
				})
		else:
			return state_query
	#again i think the below method may be redundant to the above queryset				
	def detail(request, state_id):
		state_by_id = get_object_or_404(State, pk=state_id)
		return render(request, 'fgigs/statedetail.html', {'state_by_id':state_by_id})

#################################################################

class StateAllCrewView(generic.ListView):
	"""all crew listings, for all fisheries, for one state, 
	filtered by state primary key (self.id) 
	"""
	template_name = 'fgigs/stateallcrew.html'
	context_object_name = 'state_all_crew_list'
	
	def get_queryset(self):
		try:	#put these two query sets into a list? keep as querysets in a dict?
			#still need to filter out distincts		
			home_crew_query = Crew.objects.filter(home_port_state_id=state_id)
			#only evaluate crew object if its current port is different than its home port
			current_crew_query = Crew.objects.filter(home_port_state_id=state_id)
		except(KeyError, Crew.DoesNotExist, EmptyResultSet):
			return render(request, 'fgigs/statecrewnotfound.html', {
				'error_message':"Crew for that State selection was not found.",
				})
		else:
			pkquery = home_crew_query + current_crew_query
			return pkquery 
	""" for now perhaps turn querysets to lists, don't think much beyond list functionality
	is needed right now.
	"""	
#################################################################

class StatePKView(generic.ListView):
	"""one state, filtered by primary key (self.id), includes all fisheries in state 
	"""
	template_name = 'fgigs/statepk.html'
	context_object_name = 'state_pk_list'
	
	def get_queryset(self):
		try:			
			pkquery = Fishery.objects.filter(fishery_state_id=state_id)
		except(KeyError, Fishery.DoesNotExist, EmptyResultSet):
			return render(request, 'fgigs/statenotfound.html', {
				'error_message':"That State selection was not found.",
				})
		else:
			return pkquery 
	""" how to spearate out the different state fisheries in the returned queryset
		should they display differently? different highlights? or a choice to search by fishery?
	"""	
#################################################################



class StateFisheryAllIndexView(generic.ListView):
	""" all states in a fishery 
	"""
	template_name = 'statefisheryallindex.html'
	context_object_name = 'state_fishery_all_list'
	
	def get_queryset(self):
		try:
			#each state need a list of all included fisheries
			index_query = State.objects.filter() 
		except (EmptyResultSet):
			return render(request, 'fgigs/statenotfound.html', {
				'error_message':"State was not found.",
				})
		else:
			return index_query 
			
	def get_state_list(self):
		state_query_all = self.get_queryset
		return list(state_query_all)

#################################################################


# Crew views: 	all crew in db, 
#				all crew in each fishery,
#				all crew in each state,
#				all crew in a fishery in a state
#				individual crew details,
#?

class CrewAllIndexView(generic.ListView):
	template_name = 'crewallindex.html'
	context_object_name = 'crew_all_list'
	
	def get_queryset(self):
		try:
			index_query = Crew.objects.all() 
		except(EmptyResultSet):
			return render(request, 'fgigs/crewnotfound.html', {
				'error_message':"Crew was not found.",
				})
		else:
			return index_query 
			
	def get_crew_list(self):
		crew_query_all = self.get_queryset
		return list(crew_query_all)	

#################################################################

class CrewFisheryAllIndexView(generic.ListView):
	template_name = 'crewfisheryallindex.html'
	context_object_name = 'crew_fishery_all_list'
	
	def get_queryset(self):
		try:
			index_query = Crew.objects.filter(crew_fishery=fishery_id)
		except(KeyError, Fishery.DoesNotExist, EmptyResultSet):
			return render(request, 'fgigs/crewfisherynotfound.html', {
				'error_message':"No Crew in that Fishery was found.",
				})
		else:
			return index_query

#################################################################

class CrewStateAllIndexView(generic.Listview):
	""" all crew in a single state, should filter by both home_port and current_port
	for crew listings, then return single set of all distincts """
	template_name = 'crewstateallindex.html'
	context_object_name = 'crew_state_all_list'
	
	def get_queryset(self):
		try:
			index_query = Crew.objects.filter(home_port_state=state_id | 
			current_port_state = state_id)
		except(KeyError, State.DoesNotExist, EmptyResultSet):
			return render(request, 'fgigs/crewstatenotfound.html', {
				'error_message':"No Crew in that State was found.",
				})
		else:
			return index_query

#################################################################

class CrewFisheryStateAllIndexView(generic.Listview):
	""" all crew in a fishery in a state, again crew should be filtered by home_port
	OR current_port, as well as Fishery """
	template_name = 'crewfisherystateallindex.html'
	context_object_name = 'crew_fishery_state_all_list'
	
	def get_queryset(self):
		try:
			index_query = Crew.objects.filter(home_port_state=state_id | 
			current_port_state = state_id, crew_fishery=fishery_id)
		except(KeyError, EmptyResultSet):
			return render(request, 'fgigs/crewfisherystatenotfound.html', {
				'error_message':"No Crew in that Fishery in that State was found.",
				})
		else:
			return index_query

#################################################################

class CrewDetailView(generic.DetailView):
	""" detail view of a crew listing 
	"""
	model = Crew
	template_name = 'fgigs/crewdetail/html'
	
	def get_queryset(self):
		try:
			crew_by_pkey = Crew.objects.filter(pk=crew_id)
		except(KeyError, Crew.DoesNotExist, EmptyResultSet):
			return render(request, 'fgigs/crewdetailnotfound.html', {
			'error_message':"No matching Crew listing was found.",
			})
		else:
			return crew_by_pkey
	
	def detail(request, crew_id):
		crew_by_id = get_object_or_404(Crew, pk=crew_id)
		return render(request, 'fgigs/crewdetail.html', {'crew_by_id':crew_by_id})
			
#################################################################
# add new crew listing view
# add new fishery category view
# add new state category view

#################################################################
#~ class FisheryPKIndexView(generic.ListView):
	#~ """one fishery, filtered by primary key (self.id), from all states 
	#~ """
	#~ template_name = 'fgigs/fisherypk.html'
	#~ context_object_name = 'fishery_pk_list'
	
	#~ def get_queryset(self):
		#~ """ should return all fisheries with provided PK for all states fishery
		#~ is listed in. url directing here should use named groups for capturing
		#~ kwargs. Primary Key should be 'fishery_id' """
		#~ try:
			#~ """ get queryset for pk if possible, 
			#~ if not redirect to fishery not found page 
			#~ """
			#~ pkquery = Fishery.objects.filter(pk=fishery_id)
		#~ except(KeyError, Fishery.DoesNotExist, EmptyResultSet):
			#~ """ would rather flash an error message and go back to fisheryindexall.html
			#~ but for now can make error pages i guess.  error pages: for not founds or
			#~ nothing listed situations """
			#~ return render(request, 'fgigs/fisherynotfound.html', {
				#~ 'error_message':"Fishery was not found.",
				#~ })
		#~ else:
			#~ """ so the try worked, now make sure the template has the queryset and 
			#~ renders it correctly.  
			#~ """
			#~ return pkquery 
	#~ """ how to spearate out the different state fisheries in the returned queryset
		#~ should they display differently? different states highlighted? or a choice to search by state?
	#~ """	
#~ #################################################################


# this is the class-based-views way of doing it
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
		
#~ def index(request): this is the non-class-based views way of doing it
	#~ latest_fishery_list = Fishery.objects.order_by('-pub_date')[:5]
	#~ template = loader.get_template('fgigs/index.html')
	#~ context = {'latest_fishery_list': latest_fishery_list,}
	#~ return render(request, 'fgigs/index.html', context)
	#return HttpResponse(template.render(context,request))
	#output = ','.join([f.description_text for f in latest_fishery_list])
	#return HttpResponse(output)
	#return HttpResponse("index page!")

#generic.DetailView = display page of details of one object
#generic.DetailView expects primary key as pk from URL
#generic.DetailView defaults to 'appName/modelName_detail.html for template	
class DetailView(generic.DetailView):
	model = Fishery
	#overriding the default template name, as mentioned above
	template_name = 'fgigs/detail.html'
	
	def get_queryset(self):
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
