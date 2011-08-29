import os
import sys

sys.path.append('/home/mfinkel/repos/')
sys.path.append('/home/mfinkel/repos/guarddogs/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'guarddogs.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
