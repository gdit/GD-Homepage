import datetime, calendar

from basesite import models
import eventCalBase

#
# TODO - should have used id to identify event, not rowid
#

class CalendarController(object):
    """Controller object for calendar"""
    def __init__(self, owner, day=1):
        """owner - owner of this calendar, day - day to shown"""
        calendar.setfirstweekday(calendar.SUNDAY)
        self.owner = owner
        self.day = day
        self.curr = None
        self.db_cal = None
        self.db_events = None

    ## database related operation (i.e. operation will sync with DB
    def load(self, year, month):
        """load calendar with data from database"""
        #temp = models.EventCalendar.objects.filter(owner=self.owner, 
        #        year=year, month=month)

        temp = models.EventCalendar.objects.all()
        if temp:    # either 1 record or no record , check models.py
	    if len(temp) == 1:
              self.db_cal = temp[0]
	    else:
	      for cale in temp:
	        if cale.owner == self.owner:
	          self.db_cal = cale
            self.db_events = models.RunningNight.objects.filter(cal=self.db_cal,
                    date__year=year, date__month=month)

            self.curr = eventCalBase.monthCalendar(self.db_cal.id, 
                    self.owner, year, month)
            for db_e in self.db_events:
                e = eventCalBase.event(id=db_e.id, name=db_e.name, date=db_e.date,
                        end=db_e.end, cars=db_e.cars, descr=db_e.descr, evtype=db_e.evtype)
                self.curr.addEvent(e, db_e.date.day)
        else:
            self.curr = eventCalBase.monthCalendar(None, self.owner, 
                    year, month)

    def save(self):
        """save current calendar to database"""
        # there are no edit screen so far.  Hence nothing to save. 
        #  i.e. not tested.

        # insert or update EventCalendar
        db_c = models.EventCalendar(owner=self.curr.owner,
                year=self.curr.year, month=self.curr.month)
        db_c.id = sself.curr.id
        db_c.save()

        # insert or update Events
        for d in self.curr.events:
            for e in self.curr[d]:
                db_e = models.RunningNight(cal=db_c, name=e.name, descr=e.desc,
                        date=e.start, end=e.end, cars=e.cars, evtype=e.evtype)
                db_e.id = e.id
                db_e.save()

    def addEvent(self, day, name, date, end, descr, cars, evtype):
        """Add event to the calendar.  For now change is sync to db at once."""
        if not self.db_cal:
            # we are adding event to a month where no event exist, hence
            # finally we need a EventCalendar record for the month in database
            self.db_cal = models.EventCalendar(owner=self.curr.owner,
                year=self.curr.year, month=self.curr.month)
            self.db_cal.save()
        db_e = models.RunningNight(name=name, date=date, end=end, descr=descr, cars=cars, cal=self.db_cal, evtype=evtype)
        db_e.save()

        # should have check the return above
        e = eventCalBase.event(db_e.id, db_e.name, db_e.date, db_e.end, db_e.descr, db_e.evtype)
        self.curr.addEvent(e, db_e.date.day)

    def delEvent(self, day, rowid):
        """delete an event from calendar by it's order in the GUI"""
        index = rowid - 1
        try:
            e = self.curr.events[day][index]
            db_e = models.Event.objects.get(id=e.id)
            if db_e:
                db_e.delete()
                self.curr.events[day].remove(e)
            else:
                raise ValueError, 'event (id = %d) does not exist in database'
        except KeyError:
            raise KeyError, 'invalid rowid %d' % rowid

    def updEvent(self, day, rowid, name, date, end, descr, evtype):
        """update an event from calendar"""
        index = rowid - 1
        try:
            e = self.curr.events[day][index]
            db_e = models.RunningNight.objects.get(id=e.id)
            if db_e:
                vlist = zip(('name', 'date', 'end', 'descr', evtype), (name, date, end, descr, evtype))
                for key, value in vlist:
                    for o in (db_e, e):
                        setattr(o, key, value)
                db_e.save()
        except KeyError:
            raise KeyError, 'invalid rowid %d' % rowid

    ## functions used by template
    def next(self):
        """return a tuple that contains next year and month"""
        y = self.curr.year
        m = self.curr.month
        if m == 12:
            m = 1
            y += 1
        else:
            m += 1
        return (y,m)
        
    def prev(self):
        """return a tuple that contains previous year and month"""
        y = self.curr.year
        m = self.curr.month
        if m == 1:
            m = 12
            y -= 1
        else:
            m -= 1
        return (y,m)
        
    def getWeekHeader(self):
        """return a list of week header"""
        return calendar.weekheader(2).split()

    def getMonthHeader(self):
        """return a tuple that contains abbv. month name and 4 digit year"""
        return self.curr.getDate(1).strftime("%b"), self.curr.year

    def getMonthCalendar(self):
        """return a matrix similar to calendar.monthCalendar().  Except
           the element is replaced by (day, event exist)"""
        res = []
        for dayline in calendar.monthcalendar(self.curr.year, self.curr.month):
            res_line = []
            for day in dayline:
                data = False
                if day in self.curr.events:
                    data = True
                res_line.append((day, data))
            res.append(res_line)
        return res
        
    def getDailyEvents(self):
        """return list of events for the day"""
        return self.curr.getDailyEvents(self.day)

    def hasDailyEvents(self):
        """return list of events for the day"""
        return len(self.curr.getDailyEvents(self.day)) > 0

    def getDayName(self):
        result = 'th'
        if self.day % 10 == 1 and self.day != 11:
            result = 'st'
        elif self.day % 10 == 2 and self.day != 12:
            result = 'nd'
        elif self.day % 10 == 3 and self.day != 13:
            result = 'rd'
        return result

