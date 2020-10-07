from .models import SubCategory

def shabashka_context_processor(request):
    context = {}
    context['categories'] = SubCategory.objects.all()
    return context