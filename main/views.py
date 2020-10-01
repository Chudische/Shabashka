from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.contrib.auth.views import LoginView, LogoutView 


from .models import ShaUser
# Create your views here.


def index(request):
    return render(request, "main/index.html")


# def single(request):
#     return render(request, "main/single.html")


def other_page(request, page):
    try:
        template = get_template('main/'+ page + '.html')
    except TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request))

class ShaLogin(LoginView):
    template_name = 'main/login.html'

    