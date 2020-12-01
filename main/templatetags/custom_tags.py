from django import template
from django.utils.safestring import mark_safe

from ..models import Comment

register = template.Library()

@register.simple_tag()
def time_measure(pk):
    comment = Comment.objects.get(pk=pk)
    time = comment.time_amount
    if comment.measure == 'h':
        if time == 1 or time % 10 == 1:
            return "час"
        elif time > 1 and time < 5 or time % 10 > 1 and time % 10 < 5:
            return "часа"
        elif time > 4 and time < 21 or time % 10 > 4 and time % 10 < 10:
            return "часов"
        else:
            return 'ч'
    if comment.measure == 'd':
        if time == 1 or time % 10 == 1:
            return "день"
        elif time > 1 and time < 5 or time % 10 > 1 and time % 10 < 5:
            return "дня"
        elif time > 4 and time < 21 or time % 10 > 4 and time % 10 < 10:
            return "дней"
        else:
            return 'д'
    if comment.measure == 'w':
        if time == 1 or time % 10 == 1:
            return "неделя"
        elif time > 1 and time < 5 or time % 10 > 1 and time % 10 < 5:
            return "недели"
        elif time > 4 and time < 21 or time % 10 > 4 and time % 10 < 10:
            return "недель"
        else:
            return 'н'
    if comment.measure == 'm':
        if time == 1 or time % 10 == 1:
            return "месяц"
        elif time > 1 and time < 5 or time % 10 > 1 and time % 10 < 5:
            return "месяца"
        elif time > 4 and time < 21 or time % 10 > 4 and time % 10 < 10:
            return "месяцов"
        else:
            return 'м'


@register.simple_tag()
def limit_text(content):
    if len(content) > 150:
        return content[:150] + '...'
    else:
        return content

@register.simple_tag()
def show_rating(number):
    full_star = '<i class="fa fa-star" style="color: #ddad10;"></i>'
    half_star = '<i class="fa fa-star-half-full" style="color: #ddad10;"></i>'
    empty_star = '<i class="fa fa-star-o" style="color: #ddad10;"></i>'
    try:
        number = float(number)
    except ValueError:
        return False    
          
    full = int(number)
    half = 1 if number - full > 0.1 and number - full < 0.6 else 0
    if full < round(number) and half == 0:
        full += 1
    empty = 5 - full - half        
    return mark_safe(full_star * full + half_star * half + empty_star * empty)        
   
