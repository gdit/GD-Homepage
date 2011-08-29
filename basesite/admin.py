from basesite.models import *
from django.contrib import admin

class RunningNightAdmin(admin.ModelAdmin):
  fieldsets = [
    (None, {'fields': ['name', 'date', 'end', 'evtype', 'cal',]}),
    ('Optional', {'fields': ['cars', 'svisor', 'descr']}),
  ]

  list_display = ('name', 'date', 'created', 'moded')
  list_filter = ['created']
  date_hierarchy = 'created'

admin.site.register(RunningNight, RunningNightAdmin)
admin.site.register(EventCalendar)
admin.site.register(EventType)
admin.site.register(RNPosition)
