from django.db import models
from datetime import *
import eventCalBase

# Create your models here.
class EventCalendar(models.Model):
    class Admin:
        pass

    owner = models.CharField(max_length=50)
    year = models.IntegerField()
    month = models.IntegerField()

    class Meta:
        unique_together = (('owner', 'year', 'month'),)
    
    def __str__(self):
        return 'of %s for %02d/%04d' % (
                self.owner, self.month, self.year)

class EventType(models.Model):
  evtype = models.CharField(max_length=50, help_text='Event Type, e.g. Executive Meeting, General Body Meeting, Running Night, etc')

  def __str__(self):
    return '%s' % self.evtype

class RNPosition(models.Model):
  disp = models.PositiveIntegerField(default=1)
  ra = models.PositiveIntegerField(default=1)
  driver = models.PositiveIntegerField(default=1)
  svisor = models.PositiveIntegerField(default=1)
  ocsv = models.PositiveIntegerField(default=1)

  def __str__(self):
      return 'Positions'

class SignedUp(models.Model):
  pos = [['dis', 'Dispatcher'], ['ra', 'Ride Along'], ['driver', 'Driver'],['svisor', 'Supervisor'], ['ocsv', 'On-Call Supervisor']]
  phone = models.CharField(max_length=15)
  email = models.CharField(max_length=30)
  fn = models.CharField(max_length=20)
  ln = models.CharField(max_length=20)
  gender = models.CharField(max_length=20)
  position = models.CharField(max_length=10)
  username = models.CharField(max_length=10)
  c1 = models.CharField(max_length=10,choices=pos)
  c2 = models.CharField(max_length=10,choices=pos)
  c3 = models.CharField(max_length=10,choices=pos)
  

class RunningNight(models.Model):
  class Admin:
    pass

  name = models.CharField(max_length=50, help_text='Cool name, Theme Night title, Exec Board Meeting, Gen Member Meeting, etc.')
  date = models.DateTimeField('Arrive Time')
  end = models.DateTimeField('Leave Time')
  svisor = models.CharField(max_length=30, default='', verbose_name='supervisor', blank=True)
  descr = models.TextField(default='', verbose_name='description', blank=True)
  cars = models.PositiveIntegerField(help_text='Most likely a number between 1 and 10 (usually somewhere around 6)', blank=True, default=0)
  created = models.DateTimeField('Date Created', auto_now_add=True, editable=False)
  moded = models.DateTimeField('Date Modified', auto_now=True, editable=False, null=True)
  cal =  models.ForeignKey(EventCalendar)
  evtype = models.ForeignKey(EventType, verbose_name='Event Type')
  defpos = RNPosition(disp=1, ra=1, driver=1, svisor=1, ocsv=1)
  defpos.save()
  pos = models.OneToOneField(RNPosition, default=defpos.id)
  users = models.ManyToManyField(SignedUp)

  def __str__(self):
      return 'Running %s @ %s' % (self.name, self.date)

