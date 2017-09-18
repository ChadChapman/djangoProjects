from django.contrib import admin

from .models import Fishery, Crew

# register models, tell django options desired whne registering the object
#create admin classes here
#create model admin class, then pass it as 2nd arg to admin.site.register, this
#allows changes for admin options for a model

#use this instead of separate class for crew admin?
#class CrewInLine(admin.StackedInLine):
#more compact display option
class CrewInLine(admin.TabularInLine):
	model = Crew
	extra = 3

#fishery admin class
class FisheryAdmin(admin.ModelAdmin):
	#list order here is display order in admin view
	#fields = ['description_text', 'opening_date', 'updated_date']
	#can also split into fieldsets
	fieldsets = [
		(None,	{'fields': ['description_text']}),
		#Open Date will be in seperating, header bar
		('Open Date', {'fields': ['opening_date']}),
		('Update Date', {'fields':['updated_date']}),
		#alternatively:
		#('Date Infos', {'fields':['opening_date'], 'classes': ['collapse']}),
		]
		#tells django crew objs are edited on the fishery admin page, default to 
		#specified no of fields (3 here) for crew adds
		inlines = [CrewInLine]
		#django defaults to str() for each obj, but list_display can be set also
		list_display = ('description_text', 'opening_date', 'updated_date')
		list_filter = ['updated_date']
		#users can search by this:
		search_fields = ['description_text']
admin.site.register(Fishery, FisheryAdmin)

########################################################################

#crew admin class, removed in favor of adding crew when fishery is created, probably not best way to do it

#~ class CrewAdmin(admin.ModelAdmin):
	#~ #needed or?
	#~ fieldsets = [
		#~ (None, {'fields': ['crew_text']}),
		#~ (None, {'fields': ['crew_fishery']}),
		#~ (None, {'fields': ['crew_looks']}),
		#~ ]
	#~ # end?
#~ admin.site.register(Crew)
