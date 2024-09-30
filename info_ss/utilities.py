from datetime import date, timedelta, datetime
from .models import Info_table
from django.utils import timezone


# сбор информации для стат.отчетов
def info_collect(request, **kwargs):
    try:
        visitor_tz = request.META['TZ']
    except KeyError:
        visitor_tz = ''
    if request.user.id is None:
        info = Info_table(
            date_of_visit=timezone.now(),
            visitor_IP=request.META['REMOTE_ADDR'],
            visitor_tz=visitor_tz,
            **kwargs,
        )
        info.save()
    else:
        info = Info_table(
            date_of_visit=timezone.now(),
            visitor_id=request.user.id,
            visitor_name=request.user.username,
            visitor_IP=request.META['REMOTE_ADDR'],
            visitor_email=request.user.email,
            visitor_tz=visitor_tz,
            **kwargs,
        )
        info.save()

