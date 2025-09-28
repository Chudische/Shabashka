from django import template
from django.utils.safestring import mark_safe

from ..models import Comment

register = template.Library()


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
        return None
    except TypeError:
        return None  
          
    full = int(number)
    half = 1 if number - full > 0.1 and number - full < 0.6 else 0
    if full < round(number) and half == 0:
        full += 1
    empty = 5 - full - half        
    return mark_safe(full_star * full + half_star * half + empty_star * empty)        
   

@register.filter
def in_followers(user, author):    
    count = author.followers.filter(pk=user.id).count()
    return count > 0