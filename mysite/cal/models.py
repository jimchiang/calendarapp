from django.db import models
import re, datetime, calendar


# Create your models here.
class CalEvent(models.Model):
    name = models.CharField(max_length=200)
    startDate = models.DateTimeField('startDate')
    endDate = models.DateTimeField('endDate')
    description = models.CharField(max_length=2000)
    day = models.CharField(max_length=2)



class Calendar(models.Model):

    def get_month(self,month,year):
        day = datetime.datetime.now()
        if month == 0:
            startDate=datetime.date(day.year,day.month,1)
            endDate=datetime.date(day.year,day.month, self.get_last_day(day.strftime('%B'),day.year))
            return startDate,endDate
        else:
            startDate = datetime.date(year,month,1)
            endDate = datetime.date(year,month, self.get_last_day(startDate.strftime('%B'),startDate.year))
            return startDate,endDate
    
    def get_events_by_month(self,monthStart,monthEnd):
        list1 = CalEvent.objects.filter(startDate__gte=monthStart)
        list2 = CalEvent.objects.filter(startDate__lte=monthEnd)
        return list1 & list2

    def get_last_day(self,month,year):
        month_map = { 
            'January' : 31,
            'February' : 28,
            'March' : 31,
            'April' : 30,
            'May' : 31,
            'June' : 30,
            'July' : 31,
            'August' : 31,
            'September' : 30,
            'October' : 31,
            'November' : 30,
            'December' : 31, 
            }
        if int(year) % 4 == 0:
            month_map['February'] = 29
            
        return month_map[month]
            
    def prepare_fields(self,month,days,events):
            firstDay = month[0].strftime('%A')
            lastDay = month[1].strftime('%A')
            listMonth = []
            #print firstDay
            offsetFirst=days.index(firstDay)
            offsetLast=6-days.index(lastDay)
            #print offsetFirst
            #print offsetLast
            countDays = month[0]-month[1]
            currentDay = 0;
            listWeek=[]
            while currentDay != int(month[1].strftime('%d'))+2:
                if currentDay == 0:
                    for x in range(offsetFirst):
                        listWeek.append(("",""))
                elif currentDay == int(month[1].strftime('%d'))+1:
                    for x in range(offsetLast):
                        listWeek.append(("",""))
                else:
                    tup = [];
                    for p in events:
                        if int(p.startDate.strftime('%d')) == currentDay:
                            tup.append(p)
                    listWeek.append((currentDay,tup))
                                    
                currentDay+=1
             #   print listWeek

                if len(listWeek) == 7:
                    listMonth.append(listWeek)
                    listWeek = []
            #print listMonth
            return listMonth
