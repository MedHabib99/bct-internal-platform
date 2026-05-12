from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Partner

@login_required
def index(request):
    category = request.GET.get('category', '')
    
    if category:
        partners = Partner.objects.filter(category=category)
    else:
        partners = Partner.objects.all()
    
    context = {
        'partners': partners,
        'selected_category': category,
        'categories': Partner._meta.get_field('category').choices,
    }
    return render(request, 'partners/index.html', context)

