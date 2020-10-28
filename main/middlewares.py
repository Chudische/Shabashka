from .models import SubCategory

def shabashka_context_processor(request):
    context = {}
    context['categories'] = SubCategory.objects.all()
    context['keyword'] = ''
    context['all'] = ''
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            context['keyword'] = '?keyword' + keyword
            context['all'] = context['keyword']
        if 'page' in request.GET:
            page = request.GET['page']
            if page != 1:
                if context['all']:
                    context['all'] += '&page=' + page
                else:
                    context['all'] = '?page=' + page
        
    return context