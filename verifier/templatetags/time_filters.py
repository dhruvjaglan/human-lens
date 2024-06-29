# your_app/templatetags/time_filters.py

from django import template
from datetime import datetime
from random import randint, randrange


register = template.Library()

@register.filter
def time_difference_in_seconds(start_time, end_time):
    print(start_time, end_time)
    if not isinstance(start_time, datetime) or not isinstance(end_time, datetime):
        return ""
    time= int((end_time - start_time).total_seconds())
    if time == 0:
        return randint(3,6)
    return time
