from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import InfoPage

@login_required
def index(request):
    vouchers = InfoPage.objects.filter(category='vouchers')
    company = InfoPage.objects.filter(category='company')
    tours = InfoPage.objects.filter(category='tours')
    policies = InfoPage.objects.filter(category='policies')
    benefits = InfoPage.objects.filter(category='benefits')
    
    context = {
        'vouchers': vouchers,
        'company': company,
        'tours': tours,
        'policies': policies,
        'benefits': benefits,
    }
    return render(request, 'generalinfo/index.html', context)

