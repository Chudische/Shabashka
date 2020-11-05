from django import template

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
    if comment.measure == 'd':
        if time == 1 or time % 10 == 1:
            return "день"
        elif time > 1 and time < 5 or time % 10 > 1 and time % 10 < 5:
            return "дня"
        elif time > 4 and time < 21 or time % 10 > 4 and time % 10 < 10:
            return "дней"
    if comment.measure == 'w':
        if time == 1 or time % 10 == 1:
            return "неделя"
        elif time > 1 and time < 5 or time % 10 > 1 and time % 10 < 5:
            return "недели"
        elif time > 4 and time < 21 or time % 10 > 4 and time % 10 < 10:
            return "недель"
    if comment.measure == 'm':
        if time == 1 or time % 10 == 1:
            return "месяц"
        elif time > 1 and time < 5 or time % 10 > 1 and time % 10 < 5:
            return "месяца"
        elif time > 4 and time < 21 or time % 10 > 4 and time % 10 < 10:
            return "месяцов"


@register.simple_tag()
def limit_text(content):
    if len(content) > 150:
        return content[:150] + '...'
    else:
        return content