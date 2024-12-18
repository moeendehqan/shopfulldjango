from django import template
import jdatetime

register = template.Library()

@register.filter
def to_jalali(value):
    try:
        jalali_date = jdatetime.date.fromgregorian(date=value)
        return jalali_date.strftime("%Y/%m/%d")
    except:
        return value 