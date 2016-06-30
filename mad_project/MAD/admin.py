
# Register your models here.
from django.contrib import admin
from MAD.models import Activities, Categories, act_cat, act_day

class ActivityAdmin(admin.ModelAdmin):
	list_display = ('name', 'postcode', 'contactName')

class JunctionAdmin(admin.ModelAdmin):
	list_display = ('act', 'cat')

class DaysAdmin(admin.ModelAdmin):
	list_display = ('act', 'day', 'startTime', 'endTime')

admin.site.register(Activities, ActivityAdmin)
admin.site.register(Categories)
admin.site.register(act_cat, JunctionAdmin)
admin.site.register(act_day, DaysAdmin)


