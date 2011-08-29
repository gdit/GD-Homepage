from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('basesite.views',
    url(r'^runningnight', 'runningnight'),

)
