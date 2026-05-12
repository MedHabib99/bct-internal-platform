from django.contrib.auth import logout
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta


@login_required
def home(request):
    has_new_news = False
    
    try:
        from news.models import NewsArticle
        
        now = timezone.now()
        threshold = now - timedelta(days=3)
        
        has_new_news = NewsArticle.objects.filter(
            status='published',
            publish_date__isnull=False,
            publish_date__lte=now,
            publish_date__gte=threshold
        ).exists()
    except ImportError:
        pass
    
    context = {
        'has_new_news': has_new_news,
    }
    return render(request, "home.html", context)


def logout_view(request):
    logout(request)
    return redirect("accounts:login")  

