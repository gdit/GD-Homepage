########## FOrms ###################
from django import forms

from basesite import models
class ExecSignUpForm(forms.Form):
  mempos = [['dis', 'Dispatcher'], ['ra', 'Ride Along'], ['driver', 'Driver'],['svisor', 'Supervisor'], ['ocsv', 'On-Call Supervisor']]
  first_name = forms.CharField(max_length=20, label='First Name')
  last_name = forms.CharField(max_length=20, label='Last Name')
  phone = forms.CharField(max_length=15, label='Phone Number', error_messages={'max_length' : 'Please provide a valid phone number'} )
  email = forms.EmailField(min_length=10, label='Email Address')
  gender = forms.CharField(label='Gender')
  username = forms.CharField(max_length=8, label='Username',)

  mempos.insert(0, ['na', '[First Choice]'])
  fposition = forms.ChoiceField(label='First Choice', error_messages={'required' : 'All Choices must be selected, even if they\'re all the same'})
  mempos.pop(0)
  mempos.insert(0, ['na', '(Second Choice)'])
  sposition = forms.ChoiceField(choices=mempos, label='Second Choice', error_messages={'required' : 'All Choices must be selected, even if they\'re all the same'})
  mempos.pop(0)
  mempos.insert(0, ['na', '<Third Choice>'])
  tposition = forms.ChoiceField(choices=mempos, label='Third Choice', error_messages={'required' : 'All Choices must be selected, even if they\'re all the same'})
  partner = forms.ChoiceField(label='Partner', required=False)
 
  name = forms.CharField(max_length=50, help_text='Cool name, Theme Night title, Exec Board Meeting, Gen Member Meeting, etc.',)
  date = forms.DateTimeField(label='Arrive Time',)
  end = forms.DateTimeField(label='Leave Time',)
  svisor = forms.CharField(max_length=30, label='supervisor', required=False,)
  descr = forms.CharField(label='description', required=False,)
  cars = forms.IntegerField(help_text='Most likely a number between 1 and 10 (usually somewhere around 6)', required=False,)


class GenSignUpForm(forms.Form):
  mempos = [['dis', 'Dispatcher'], ['ra', 'Ride Along'], ['driver', 'Driver']]

  first_name = forms.CharField(max_length=20, label='First Name')
  last_name = forms.CharField(max_length=20, label='Last Name')
  phone = forms.CharField(max_length=15, label='Phone Number', error_messages={'max_length' : 'Please provide a valid phone number'})
  email = forms.EmailField(min_length=10, label='Email Address')
  gender = forms.CharField(label='Gender')
  username = forms.CharField(max_length=8, label='Username',)
  
  mempos.insert(0, ['na', '[First Choice]'])
  fposition = forms.ChoiceField(label='First Choice', error_messages={'required' : 'All Choices must be selected, even if they\'re all the same'})
  mempos.pop(0)
  mempos.insert(0, ['na', '(Second Choice)'])
  sposition = forms.ChoiceField(choices=mempos, label='Second Choice', error_messages={'required' : 'All Choices must be selected, even if they\'re all the same'})
  mempos.pop(0)
  mempos.insert(0, ['na', '<Third Choice>'])
  tposition = forms.ChoiceField(choices=mempos, label='Third Choice', error_messages={'required' : 'All Choices must be selected, even if they\'re all the same'})
  mempos.pop(0)
  partner = forms.ChoiceField(label='Partner', required=False)
