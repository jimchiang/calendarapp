# Create your views here.
from django.template import Context, loader
from cal.models import CalEvent
from django.http import HttpResponse
import re, datetime, calendar

def index(request):
    t=loader.get_template('cal/index.html')
    if request.method == 'GET' and 'month' in request.GET and 'year' in request.GET:
        month = get_month(int(request.GET['month']),int(request.GET['year']))
    else:
        month = get_month(0,0)
        
    events = get_events_by_month(month[0],month[1])
    #print events
    days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    fields = prepare_fields(month,days,events);
    c= Context({
            'name' : month[0].strftime('%B %Y'),
            'month': month,
            'days' : days,
            'fields' : fields
            })
    return HttpResponse(t.render(c))

def get_month(month,year):
    day = datetime.datetime.now()
    if month == 0:
        startDate=datetime.date(day.year,day.month,1,00,00)
        endDate=datetime.date(day.year.day.month,get_last_day(day.strftime('%B'),day.year),23,59)
        return startDate,endDate
    else:
        startDate = datetime.date(year,month,1)
        endDate = datetime.date(year,month,get_last_day(startDate.strftime('%B'),startDate.year))
        return startDate,endDate
    
def get_events_by_month(monthStart,monthEnd):
    list1 = CalEvent.objects.filter(startDate__gte=monthStart)
    list2 = CalEvent.objects.filter(startDate__lte=monthEnd)
    return list1 & list2

def get_last_day(month,year):
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

def prepare_fields(month,days,events):
    firstDay = month[0].strftime('%A')
    lastDay = month[1].strftime('%A')
    listMonth = []
    print firstDay
    offsetFirst=days.index(firstDay)
    offsetLast=6-days.index(lastDay)
    print offsetFirst
    print offsetLast
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
        #print listWeek
        if len(listWeek) == 7:
            listMonth.append(listWeek)
            listWeek = []
    return listMonth
