# Create your views here.
#from django.conf.urls.defaults import *
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from datetime import date
from cal import views 
from basesite import newforms

ap = 'basesite/about' #about path
mp = 'basesite/members' #member path
sp = 'basesite/sponsors' #Sponsors path
cp = 'basesite/contact'  #Contact path
INCLUDE_MEMNAV = '/home/mfinkel/djangotest/mem/templates/basesite/members/memnav'
INCLUDE_SPONNAV = '/home/mfinkel/djangotest/mem/templates/basesite/sponsors/sponnav'
INCLUDE_CONNAV = '/home/mfinkel/djangotest/mem/templates/basesite/contact/connav'


########## Misc Functions #############

def getEv(evdate, evtype):
  import models
  import datetime

  rn = models.RunningNight.objects.all()
  if len(rn) > 0:
    for ev in rn:
      if ev.date.date() == datetime.date(int(evdate[0]), int(evdate[1]), int(evdate[2])):
        if ev.evtype.evtype == evtype:
	  return ev

#######

def setPosition(evdate):
  ev = getEv(evdate,'Running Night')
  if ev:
    cars = ev.cars
    positions = ev.pos
    cars = int(cars)
    if cars > 1:
      positions.disp = 4
      positions.ra = cars
      positions.driver = cars
      positions.save()
      return (ev, positions)

########3

def firsttimesignup(ev, un):
  users = ev.users.all()
  for user in users:
    if user.username == un:
      return False
  return True

########

def getFilledPositions(ev):
  users = ev.users.all()
  dis = driver = ra = 0
  for user in users:
    if user.c1 == 'dis':
      dis = dis + 1
    elif user.c1 == 'ra':
      ra = ra + 1
    elif user.c1 == 'driver':
      driver = driver + 1
  return (dis, driver, ra) #always returns values in this order

########

def setPositionsLeft(dis, driver, ra, pos):
  return (pos.disp - dis, pos.driver - driver, pos.ra - ra)

########

def getChoiceList(dis, driver, ra):
  choice = []
  if dis:
    choice.append(['dis', 'Dispatcher'])
  if driver:
    choice.append(['driver', 'Driver'])
  if ra:
    choice.append(['ra', 'Ride Along'])
  if choice:
    return choice
  else:
    return false

########

def getExecChoiceList(c1, ev):
  svisor = ocsv = 0
  sv = ""
  for user in ev.users.all():
    if user.c1 == 'svisor':
      svisor = svisor + 1
      sv = user.fn + " " + user.ln
    if user.c1 == 'ocsv':
      ocsv = ocsv + 1
  if not svisor:
    c1.append(['svisor', 'Supervisor'])
  if ocsv:
    c1.append(['ocsv', 'On-Call Supervisor'])
  if sv:
    ev.svisor = sv
    ev.save()
  return c1

########

def updateinfo(ev, username, signup):
  for user in ev.users.all():
    if user.username == username:
      user.phone = signup.phone
      user.email = signup.email
      user.fn = signup.fn
      user.ln = signup.ln
      user.gender = signup.gender
      user.c1 = signup.c1
      user.c2 = signup.c2
      user.c3 = signup.c3
      user.save()

#########

def loginoutauth(request):
  import login
  events = views.view(request)
  if request.method == 'POST':
    if 'submit' in request.POST:
      if request.POST['submit'] == 'logout':
        login.inside_logout(request)
      elif request.POST['submit'] == 'login':
        user = login.inside_login(request)
        if user != None:
          if request.user.is_authenticated():
            c = RequestContext(request, {})
	    c.update(events)
            return render_to_response('basesite/index.html', c)
        else:
          if request.user.is_authenticated():
            c = RequestContext(request, {})
	    c.update(events)
            return render_to_response('basesite/index.html', c)

##########

def checkSignedUpForm(request):
  import models
  if request.method == 'POST':
    loginoutauth(request)
    if 'su' in request.POST:
      if request.POST['su'] == 'e':
        form = newforms.ExecSignUpForm(request.POST)
      elif request.POST['su'] == 'g':
        form = newforms.GenSignUpForm(request.POST)
      if form.is_valid():
        evdate = request.path[1:].split('/')
        form.full_clean()
        ev = getEv(evdate, 'Running Night')
	newuser = models.SignedUp(fn = form.cleaned_data['first_name'],
          ln = form.cleaned_data['last_name'], 
          phone = form.cleaned_data['phone'], 
          email = form.cleaned_data['email'], 
          gender = form.cleaned_data['gender'], 
          username = form.cleaned_data['username'], 
          c1 = form.cleaned_data['fposition'], 
          c2 = form.cleaned_data['sposition'], 
          c3 = form.cleaned_data['tposition'],)
	newuser.save()
	if firsttimesignup(ev, form.cleaned_data['username']):
  	  ev.users.add(newuser)
	else:
	  updateinfo(ev, form.cleaned_data['username'], newuser)

	if request.user.has_perm('mem.change_RunningNight'):
	  ev.name = form.cleaned_data['name']
	  ev.date = form.cleaned_data['date']
	  ev.end = form.cleaned_data['end']
	  ev.svisor = form.cleaned_data['svisor']
	  ev.descr = form.cleaned_data['descr']
	  ev.cars = form.cleaned_data['cars']
	  ev.save()
	  return ev
      else:
	return form.errors
	  
##########

def getUserInfo(user, ev):
  for evuser in ev.users.all():
    if evuser.username == user.username:
      return evuser

#########


########## Views #####################


def index(request):
  #if not request.is_secure():
   # print 'Not Secure'
    #return redirect(''.join(['https://', request.META['SERVER_NAME'], request.path_info]))
  ret = loginoutauth(request)
  if ret:
    return ret
  events = views.view(request)
  c = RequestContext(request, {})
  c.update(events)
  return render_to_response('basesite/index.html', c)
    

###################### About Pages ##################

def about(request):
  return render_to_response('/'.join([ap, 'about.html']), RequestContext(request,{}))

def history(request):
  return render_to_response('/'.join([ap, 'history.html']), RequestContext(request,{}))

def services(request):
  return render_to_response('/'.join([ap, 'services.html']), RequestContext(request,{}))

def cal(request):
  return render_to_response('/'.join([ap, 'cal.html']), RequestContext(request,{}))

def stats(request):
  return render_to_response('/'.join([ap, 'stats.html']), RequestContext(request,{}))

def financial(request):
  return render_to_response('/'.join([ap, 'financial.html']), RequestContext(request,{}))
 
def faq(request):
  return render_to_response('/'.join([ap, 'faq.html']), RequestContext(request,{}))
  
def sister(request):
  return render_to_response('/'.join([ap, 'sister.html']), RequestContext(request,{}))

def friends(request):
  return render_to_response('/'.join([ap, 'friends.html']), RequestContext(request,{}))


################## Members Pages ###################

def members(request):
  return render_to_response('/'.join([mp, 'members.html']), RequestContext(request,{}))

def executive(request):
  return render_to_response('/'.join([mp, 'executive.html']), RequestContext(request,{}))

def join(request):
  return render_to_response('/'.join([mp, 'join.html']), RequestContext(request,{}))


############## Sponsors #####################

def sponsors(request):
  return render_to_response('/'.join([sp, 'sponsors.html']), RequestContext(request,{}))

def newsponsors(request):
  return render_to_response('/'.join([sp, 'newsponsors.html']), RequestContext(request,{}))

def donate(request):
  return render_to_response('/'.join([sp, 'donate.html']), RequestContext(request,{}))


############## Contact ###################

def contact(request):
  return render_to_response('/'.join([cp, 'contact.html']), RequestContext(request,{}))


def runningnight(request):
  return render_to_response('basesite/cal.html')

############### Calendar ################

def day(request, year, month, day):
  from cal import eventCalBase
  import models

  errors = checkSignedUpForm(request) # check POST values
  events = views.view(request) # get RunningNight event, if exists

  evdate = request.path[1:].split('/')
  evpos = setPosition(evdate)
  if evpos:
    ev = evpos[0]
    pos = evpos[1]
  else:
    ev = pos = None

  if request.user.is_authenticated():
    user = request.user
    contxt = {'evdate' : evdate, 'events' : events, 'errors' : errors, 'update' : False,}
    if ev and pos: # Event exists and positions exist (which means it's a Running Night
      dis, driver, ra = getFilledPositions(ev)
      dis, driver, ra = setPositionsLeft(dis, driver, ra, pos)
      c1 = getChoiceList(dis, driver, ra)
      if firsttimesignup(ev, user.username):
        if c1:
	  ce1 = getExecChoiceList(c1, ev)
        execform = newforms.ExecSignUpForm(initial={'username' : user, 'name' : ev.name, 'date' : ev.date, 'end' : ev.end, 'svisor' : ev.svisor, 'descr' : ev.descr, 'cars' : ev.cars, 'signedupcount' : ev.users.count(), 'fposition' : ce1,})
        genform = newforms.GenSignUpForm(initial={'username' : user, 'fposition' : c1,})
      else:
        info = getUserInfo(user, ev)
        execform = newforms.ExecSignUpForm(initial={'first_name' : info.fn, 'last_name' : info.ln, 'phone' : info.phone, 'email' : info.email, 'gender' : info.gender, 'fposition' : info.c1, 'sposition' : info.c2, 'tposition' : info.c3, 'username' : user, 'name' : ev.name, 'date' : ev.date, 'end' : ev.end, 'svisor' : ev.svisor, 'descr' : ev.descr, 'cars' : ev.cars, 'signedupcount' : ev.users.count(),})
	contxt['update'] = True
        genform = 'No More Events This Day. You have already signed up for this one.'
      contxt['svisor'] = ev.svisor
      contxt['members'] = ev.users.all()
      contxt['signedupcount'] = ev.users.count()
    else:
      genform = execform = 'No Events This Day'
    contxt['execform'] = execform
    contxt['genform'] = genform
    contxt['events'] = events['cal'].curr.events[int(day)]
    c = RequestContext(request, contxt)
    c.update(events)
  else:
    if events['cal'].curr.events:
      c = RequestContext(request, {'evdate' : evdate, 'events' : events['cal'].curr.events[int(day)],})
    else:
      c = RequestContext(request, {'evdate' : evdate,})
    c.update(events)
  return render_to_response('basesite/eventdet.html', c)


def daymembers(request, year, month, day):
  if request.method == 'POST':
    if request.user.is_authenticated:
      if request.user.has_perm('mem.change_RunningNight'):
        evdate = request.path[1:].split('/')
        evpos = setPosition(evdate)
        ev = evpos[0]
	users = ev.users.all()
	temp = []
	for user in users:
	  if user.username == request.POST['remove']:
	    temp = user
	temp.delete()
        
  if request.user.is_authenticated:
    evdate = request.path[1:].split('/')
    evpos = setPosition(evdate)
    ev = evpos[0]
    c = RequestContext(request, {'evdate' : evdate, 'signedupcount' : ev.users.count(), 'members' : ev.users.all()})
  else:
    c = RequestContext(request, {})
  return render_to_response('basesite/eventmembers.html', c)
    
  


########### Login ################

########## get 404 ###############

def get404(request):
  return render_to_response('basesite/404.html')
  


