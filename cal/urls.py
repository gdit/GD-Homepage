from django.conf.urls.defaults import *

from djangoEventCal.cal.controller import CalendarController
from djangoEventCal.cal.models import Event

## calendar view
urlpatterns = patterns('cal.views',
    (r'^view/.*$', 'view'),
    (r'^upd/.*$', 'updEvent'),
    (r'^add/.*$', 'addEvent'),
    (r'^del/.*$', 'delEvent'),
    (r'^.*$', 'view'),
)

