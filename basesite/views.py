# Create your views here.
#from django.conf.urls.defaults import *
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from datetime import date
from cal import views 
from basesite import newforms
from django import forms

ap = 'basesite/about' #about path
mp = 'basesite/members' #member path
sp = 'basesite/sponsors' #Sponsors path
cp = 'basesite/contact'  #Contact path

########## Misc Functions #############

def getEv(evdate, evtype):
  """
  Function: getEv
  Parameters:
  @evdate: List with year, month, day 
  @evtype: String describing the type

  Returns Event object
  """
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
  """
  Function: setPosition
  Parameters:
  @evdate: list with year, month day

  Returns the Event model object and positions
  """
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
  """
  Function: firstimesignup
  Parameters:
  @ev: Event model object
  @un: username

  Returns True if the user has not previously signed up for event
  Returns False if the user is returning
  """
  users = ev.users.all()
  for user in users:
    if user.username == un:
      return False
  return True

########

def getFilledPositions(ev, choice):
  """
  Function: getFilledPosition
  Parameters:
  @ev: Event model object
  @choice: Choice (first=1, second, third)

  Returns a tuple containing the number of members signed up for each position
  """
  users = ev.users.all()
  #Initiate positions to zero
  dis = driver = ra = 0
  #If first choice
  if choice == 1:
    for user in users:
      if user.c1 == 'dis':
        dis = dis + 1
      elif user.c1 == 'ra':
        ra = ra + 1
      elif user.c1 == 'driver':
        driver = driver + 1
  
  #If second choice
  if choice == 2:
    for user in users:
      if user.c2 == 'dis':
        dis = dis + 1
      elif user.c2 == 'ra':
        ra = ra + 1
      elif user.c2 == 'driver':
        driver = driver + 1
  
  #If third choice
  if choice == 3:
    for user in users:
      if user.c3 == 'dis':
        dis = dis + 1
      elif user.c3 == 'ra':
        ra = ra + 1
      elif user.c3 == 'driver':
        driver = driver + 1
  return (dis, driver, ra) #always returns values in this order

########

def setPositionsLeft(dis, driver, ra, pos):
  """
  Function: setPositionsLeft
  Parameters:
  @dis: Number of dispatchers
  @driver: Number of drivers
  @ra: Number of ride along
  @pos: PNPosition model object

  Returns tuple of remaining open positions
  """
  return (pos.disp - dis, pos.driver - driver, pos.ra - ra)

########

def getChoiceList(dis, driver, ra):
  """
  Function: getChoiceList
  Parameters:
  @dis: Number of dispatchers
  @driver: Number of drivers
  @ra: Number of ride alongs

  Returns a list used for the drop-down list of available spots 
  """
  choice = []
  if dis:
    tpos = ''
    tpos = tpos.join(["Dispatcher", " (", str(dis), ")"])
    choice.append(['dis', tpos])
  if driver:
    tpos = ''
    tpos = tpos.join(["Driver", " (", str(driver), ")"])
    choice.append(['driver', tpos])
  if ra:
    tpos = ''
    tpos = tpos.join(["Ride Along", " (", str(ra), ")"])
    choice.append(['ra', tpos])
  #If dis or driver or ra contain data
  if choice[0]:
    return choice
  else:
    return false

########

def getExecChoiceList(c1, ev, curruser):
  """
  Function: getExecChoiceList
  Parameters:
  @c1: choice list
  @ev: Event model object
  @curruser: django.contrib.auth.models.User object

  Returns an altered position choice list for Exec Board Members
  """
  #Initialize variables
  svisor = ocsv = 0
  sv = ""
  for user in ev.users.all():
    if user.c1 == 'svisor':
      svisor = svisor + 1
      sv = user.fn + " " + user.ln
      svname = user.username
    if user.c1 == 'ocsv':
      ocsv = ocsv + 1
  #If supervisor has not yet been assigned or curruser is assigned as svisor
  if not svisor or svname == curruser.username:
    c1.append(['svisor', 'Supervisor'])
  c1.append(['ocsv', 'On-Call Supervisor'])
  #If sv is set above but it is not set in Event object
  if sv and not ev.svisor:
    ev.svisor = sv
    ev.save()
  return c1

########

def getCurrentSignups(ev, curruser):
  """
  Function: getCurrentSignups
  Parameters:
  @ev: Event model object
  @curruser: django.contrib.auth.models.User object

  Return list of current users signed up for event
  """
  #Initialize with list of empty string, append with all signed up members
  signedup = [['', '']]
  for user in ev.users.all():
    if user.username != curruser.username:
      if not user.partner or user.partner == curruser.username:
        signedup.append([user.username, user.username]);
  return signedup

########

def getCurrentPosition(ev, curruser):
  """
  Function: getCurrentPosition
  Parameters:
  @ev: Event model object
  @curruser: django.contrib.auth.models.User object
 
  Returns tuple of first, second, and third choices
  """
  for user in ev.users.all():
    if user.username == curruser.username:
      return (user.c1, user.c2, user.c3)

########

def checkPartnerVerified(ev, curruser):
  """
  Function: checkPartnerVerified
  Parameters:
  @ev: Event model object
  @curruser: django.contrib.auth.models.User object

  Returns Verified or Unverified
  """
  for user in ev.users.all():
    #If partnering is mutual
    if user.partner == curruser.username and user.username == curruser.partner:
      return "Verified"
  return "Unverified"

########

def checkPartnerRequested(ev, curruser):
  """
  Function: checkPartnerRequested
  Parameters:
  @ev: Event model object
  @curruser: django.contrib.auth.models.User object

  Returns username if another member has selected curruser as a partner, false otherwise
  """
  for user in ev.users.all():
    if user.partner == curruser.username:
      return user.username
  return False
  
########

def getPartner(ev, curruser):
  """
  Function: getPartner
  Parameters:
  @ev: Event model object
  @curruser: django.contrib.auth.models.User object

  Returns curruser's partner
  """
  for user in ev.users.all():
    if user.username == curruser.username:
      return user.partner
  
########

def getUserSUInfo(ev, curruser):
  """
  Function: getUserSUInfo
  Parameters:
  @ev: Event model object
  @curruser: django.contrib.auth.models.User object

  Returns SignedUp model object
  """
  for user in ev.users.all():
    if user.username == curruser.username:
      return user

########

def updateinfo(ev, username, signup):
  """
  Function: updateinfo
  Parameters:
  @ev: Event model object
  @curruser: django.contrib.auth.models.User object
  @signup: SignedUp model object

  Update existing member information for event

  Returns void
  """
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
      user.partner = signup.partner
      user.save()

#########

def loginoutauth(request):
  """
  Function: loginoutauth
  Parameters:
  @request: Client request

  Return index.html page and log user in or out, depending on current status
  """
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
          c3 = form.cleaned_data['tposition'],
	  partner = form.cleaned_data['partner'],)
	newuser.save()
	if firsttimesignup(ev, form.cleaned_data['username']):
  	  ev.users.add(newuser)
	else:
	  updateinfo(ev, form.cleaned_data['username'], newuser)

	if request.user.has_perm('mem.change_runningnight'):
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
    if 'part' in request.POST:
      form = newforms.PartnerForm(request.POST)
      if form.is_valid():
        evdate = request.path[1:].split('/')
        form.full_clean()
        ev = getEv(evdate, 'Running Night')
	user = getUserSUInfo(ev, request.user)
	user.partner = form.cleaned_data['partner']
	user.save()
        return ev
	
##########

def getUserInfo(user, ev):
  for evuser in ev.users.all():
    if evuser.username == user.username:
      return evuser

#########


########## Views #####################


def index(request):
  if not request.is_secure():
    print 'Not Secure'
    return redirect(''.join(['https://', request.META['SERVER_NAME'], request.path_info]))
  ret = loginoutauth(request)
  if ret:
    return ret
  events = views.view(request)
  c = RequestContext(request, {})
  c.update(events)
  return render_to_response('basesite/index-spon.html', c)
    

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
  #return render_to_response('basesite/construction.html', RequestContext(request,{}))
 
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

def application(request):
  appform = newforms.ApplicationForm()
  return render_to_response('/'.join([mp, 'application.html']), RequestContext(request,{'appform' : appform}))

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

def newevent(request):
  return redirect('admin/basesite/runningnight/add/')

############## Blogs ###################

def opblog(request):
  return render_to_response('basesite/opblog-const.html', RequestContext(request,{}))

def memblog(request):
  return render_to_response('basesite/memblog-const.html', RequestContext(request,{}))



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
      dis, driver, ra = getFilledPositions(ev, 1)
      dis, driver, ra = setPositionsLeft(dis, driver, ra, pos)
      c1 = getChoiceList(dis, driver, ra)
      dis, driver, ra = getFilledPositions(ev, 2)
      dis, driver, ra = setPositionsLeft(dis, driver, ra, pos)
      c2 = getChoiceList(dis, driver, ra)
      dis, driver, ra = getFilledPositions(ev, 3)
      dis, driver, ra = setPositionsLeft(dis, driver, ra, pos)
      c3 = getChoiceList(dis, driver, ra)
      if c1:
        ce1 = getExecChoiceList(c1[:], ev, user) #Need to send c1 slice as param or else will also modify (and append) c1
      if c2:
        ce2 = getExecChoiceList(c2[:], ev, user)
      if c3:
        ce3 = getExecChoiceList(c3[:], ev, user)
#      partners = getCurrentSignups(ev, user)
      partner = getPartner(ev, user)
      if firsttimesignup(ev, user.username):
        if ce1 or ce2 or ce3:
          execform = newforms.ExecSignUpForm(initial={'username' : user, 'name' : ev.name, 'date' : ev.date, 'end' : ev.end, 'svisor' : ev.svisor, 'descr' : ev.descr, 'cars' : ev.cars, 'signedupcount' : ev.users.count(),})
	  execform.fields['fposition'].choices = ce1
	  execform.fields['sposition'].choices = ce2
	  execform.fields['tposition'].choices = ce3
          execform.fields['partner'] = forms.ChoiceField(choices=getCurrentSignups(ev, user), label='Partner', required=False, help_text="Optional, to choose other member if they have already signed up for a position")
#	  execform.fields['partner'].choices = partners
        if c1 or c2 or c3:
	  genform = newforms.GenSignUpForm(initial={'username' : user,})
	  genform.fields['fposition'] = forms.ChoiceField(label='First Choice', error_messages={'required' : 'All Choices must be selected, even if they\'re all the same'})

	  #genform.fields['sposition'].choices = c2
	  #genform.fields['tposition'].choices = c3
	  genform.fields['fposition'].choices = c1
	  genform.fields['sposition'].choices = c2
	  genform.fields['tposition'].choices = c3
          genform.fields['partner'] = forms.ChoiceField(choices=getCurrentSignups(ev, user), label='Partner', required=False, help_text="Optional, to choose other member if they have already signed up for a position")
#	  genform.fields['partner'].choices = partners
	else:
          genform = 'There Are No More Open Positions. Hopefully you can find another opportunity that fits into your schedule'
      else:
        c1, c2, c3 = getCurrentPosition(ev, user)
        info = getUserInfo(user, ev)
        execform = newforms.ExecSignUpForm(initial={'first_name' : info.fn, 'last_name' : info.ln, 'phone' : info.phone, 'email' : info.email, 'gender' : info.gender, 'fposition' : info.c1, 'sposition' : info.c2, 'tposition' : info.c3, 'username' : user, 'name' : ev.name, 'date' : ev.date, 'end' : ev.end, 'svisor' : ev.svisor, 'descr' : ev.descr, 'cars' : ev.cars, 'signedupcount' : ev.users.count(), 'fposition' : c1, 'sposition' : c2, 'tposition' : c3,})
        execform.fields['partner'] = forms.ChoiceField(choices=getCurrentSignups(ev, user), initial=partner, label='Partner', required=False, help_text="Optional, to choose other member if they have already signed up for a position",)
	execform.fields['fposition'].choices = ce1
	execform.fields['sposition'].choices = ce2
	execform.fields['tposition'].choices = ce3
#	execform.fields['partner'].choices = partners
	contxt['update'] = True
        genform = "No More Events This Day. You have already signed up for this one."
	part = checkPartnerRequested(ev, user)
	if part:
	  if checkPartnerVerified(ev, user) == "Unverified":
	    gfchoosepart = "You have already signed up for this event but you also have an outstanding request from another member ({0}) to be partners. You may accept this request below by selecting them from the list below.".format(part)
	    pf = newforms.PartnerForm()
	    a = getCurrentSignups(ev, user)
	    pf.fields['partner'] = forms.ChoiceField(choices=getCurrentSignups(ev, user), initial=part, label='Partner', required=False)
	    contxt['gfchoosepart'] = gfchoosepart
	    contxt['partnerform'] = pf
	contxt['verifiedpartner'] = checkPartnerVerified(ev, user)
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
  """
  Function: daymembers
  Paramerts:
  @request: Client request
  @year: Event year
  @month: Event month
  @day: Event day

  Return info of members that signed up for event
  These values are added into a table for Exec members' use
  """
  #If form is returned with values
  if request.method == 'POST':
    #If user is logged in
    if request.user.is_authenticated:
      #If user is permission to change entires
      if request.user.has_perm('basesite.change_runningnight'):
	#Recover date from URL
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

def daymemberedit(request, year, month, day, username):
  """
  Function: daymemberedit
  Parameters: 
  @request: Client request
  @year: Event year
  @month: Event month
  @day: Rvent day
  @username: Member info for event

  Return editable form with member infomation for specific event
  which can be edited by an Exec member
  """
  if request.method == 'POST': #If form is returned with values
    import models
    if request.user.is_authenticated: #If user is logged in
      #If user has permission to edit event values
      if request.user.has_perm('basesite.change_runningnight'): 
        form = newforms.ExecSignUpForm(request.POST)
	#Check that the form fields are valid
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
            c3 = form.cleaned_data['tposition'],
	    partner = form.cleaned_data['partner'],)
	  newuser.save()
	  #Update info the original member entered
	  updateinfo(ev, form.cleaned_data['username'], newuser)
	        
  #If user is logged in
  if request.user.is_authenticated:
    #Recover date from URL
    evdate = request.path[1:].split('/')
    evpos = setPosition(evdate)
    # event Object
    ev = evpos[0]
    #Position object
    pos = evpos[1]
    #Returns how many first choice positions have been reserved
    dis, driver, ra = getFilledPositions(ev, 1)
    #Returns the number of remaining positions for first choice for each position
    dis, driver, ra = setPositionsLeft(dis, driver, ra, pos)
    #Set drop-down menu
    c1 = getChoiceList(dis, driver, ra)
    #Same as above for second choice
    dis, driver, ra = getFilledPositions(ev, 2)
    dis, driver, ra = setPositionsLeft(dis, driver, ra, pos)
    c2 = getChoiceList(dis, driver, ra)
    #Same for third choice
    dis, driver, ra = getFilledPositions(ev, 3)
    dis, driver, ra = setPositionsLeft(dis, driver, ra, pos)
    c3 = getChoiceList(dis, driver, ra)
    #Check if member has already picked a partner, either another member or ""
    for user in ev.users.all():
      if user.username == username:
        info = user
        partner = user.partner
    #Fill member's info
    execform = newforms.ExecSignUpForm(initial={'first_name' : info.fn, 'last_name' : info.ln, 'phone' : info.phone, 'email' : info.email, 'gender' : info.gender, 'fposition' : info.c1, 'sposition' : info.c2, 'tposition' : info.c3, 'username' : info.username, 'name' : ev.name, 'date' : ev.date, 'end' : ev.end, 'svisor' : ev.svisor, 'descr' : ev.descr, 'cars' : ev.cars, 'signedupcount' : ev.users.count(), 'fposition' : c1, 'sposition' : c2, 'tposition' : c3,})
    execform.fields['partner'] = forms.ChoiceField(choices=getCurrentSignups(ev, user), initial=partner, label='Partner', required=False, help_text="Optional, to choose other member if they have already signed up for a position",)
    execform.fields['fposition'].choices = c1
    execform.fields['sposition'].choices = c2
    execform.fields['tposition'].choices = c3
    c = RequestContext(request, {'evdate' : evdate, 'signedupcount' : ev.users.count(), 'execform' : execform,})
  else:
    #If not logged in, return nothing
    c = RequestContext(request, {})
  return render_to_response('basesite/eventmemberedit.html', c)

########### Login ################

########## get 404 ###############

def get404(request):
  """
  Function: get404
  Parameters:
  @request: Client request

  Return 404.html
  """
  return render_to_response('basesite/404.html')
