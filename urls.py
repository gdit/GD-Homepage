from django.conf.urls.defaults import patterns, include, url
from django.views.static import * 
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mem.views.home', name='home'),
    # url(r'^mem/', include('mem.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # Required to make static serving work 
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    #url(r'^woof', 'basesite.views.auth'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login', 'django.contrib.auth.views.login', {'template_name': 'templates/basesite/auth_index.html'}),
    url(r'^index', 'basesite.views.index'),
    #url(r'^about', 'basesite.views.about'),
    url(r'^$', 'basesite.views.index'),
)

urlpatterns += patterns('basesite.views',
  url(r'^about', 'about'),
  url(r'^history', 'history'),
  url(r'^services', 'services'),
  url(r'^cal', 'cal'),
  url(r'^services', 'services'),
  url(r'^stats', 'stats'),
  url(r'^faq', 'faq'),
  url(r'^financial', 'financial'),
  url(r'^sister', 'sister'),
  url(r'^friends', 'friends'),
)    

urlpatterns += patterns('basesite.views',
  url(r'^members', 'members'),
  url(r'^executive', 'executive'),
  url(r'^join', 'join'),
)

urlpatterns += patterns('basesite.views',
  url(r'^sponsors', 'sponsors'),
  url(r'newsponsors', 'newsponsors'),
  url(r'donate', 'donate'),
)

urlpatterns += patterns('basesite.views',
  url(r'contact', 'contact'),
)

urlpatterns += patterns('basesite.views',
  url(r'(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/members.html', 'daymembers'),
  url(r'(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)', 'day'),
  
)

urlpatterns += patterns('',
  url(r'opblog', include('opblog.mingus.urls')),
)

#####ALWAYS LAST#####
urlpatterns += patterns('basesite.views',
  url(r'.+', 'get404'),
)
