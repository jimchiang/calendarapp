# Create your views here.
from django.template import Context, loader
from cal.models import CalEvent
from django.http import HttpResponse
import re, datetime, calendar
from cal.models import Calendar

def index(request):
    t=loader.get_template('cal/index.html')
    cal = Calendar()
    if request.method == 'GET' and 'month' in request.GET and 'year' in request.GET:
        month = cal.get_month(int(request.GET['month']),int(request.GET['year']))
    else:
        month = cal.get_month(0,0)
        
    events = cal.get_events_by_month(month[0],month[1])
    #print events
    days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    fields = cal.prepare_fields(month,days,events);
    print fields
    c= Context({
            'name' : month[0].strftime('%B %Y'),
            'month': month,
            'days' : days,
            'fields' : fields
            })
    return HttpResponse(t.render(c))

def detail(request,cal_id):
    event = CalEvent.objects.filter(id__exact=cal_id)
    return HttpResponse(event[0].startDate)
