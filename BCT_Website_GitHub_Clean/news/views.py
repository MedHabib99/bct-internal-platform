from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from .models import NewsArticle, NewsCategory
from .forms import NewsForm


def is_teamleader(user):
    return (
        user.is_authenticated and (
            user.is_superuser or
            user.is_staff or
            user.groups.filter(name__iexact='teamleader').exists()
        )
    )


@login_required
def index(request):
    category_slug = request.GET.get('category', '')
    user_is_teamleader = is_teamleader(request.user)
    
    if user_is_teamleader:
        if category_slug:
            articles = NewsArticle.objects.filter(category__slug=category_slug)
        else:
            articles = NewsArticle.objects.all()
        
        articles = articles.order_by(
            '-is_important',
            '-status',
            '-publish_date',
            '-created_at'
        )
    else:
        now = timezone.now()
        articles_query = NewsArticle.objects.filter(
            status='published',
            publish_date__lte=now
        )
        
        if category_slug:
            articles_query = articles_query.filter(category__slug=category_slug)
        
        articles = articles_query.order_by('-is_important', '-publish_date')
    
    categories = NewsCategory.objects.all()
    
    context = {
        'articles': articles,
        'selected_category': category_slug,
        'categories': categories,
        'is_teamleader': user_is_teamleader,
    }
    return render(request, 'news/index.html', context)


@login_required
def detail(request, pk):
    article = get_object_or_404(NewsArticle, pk=pk)
    user_is_teamleader = is_teamleader(request.user)
    
    if article.status == 'draft' and not user_is_teamleader:
        messages.error(request, "You don't have permission to view this article.")
        return redirect('news:index')
    
    if not user_is_teamleader and article.publish_date and article.publish_date > timezone.now():
        messages.error(request, "This article is not yet available.")
        return redirect('news:index')
    
    context = {
        'article': article,
        'is_teamleader': user_is_teamleader,
    }
    return render(request, 'news/detail.html', context)


@login_required
def create_news(request):
    if not is_teamleader(request.user):
        messages.error(request, "Only Team Leaders can create news articles.")
        return redirect('news:index')
    
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.created_by = request.user
            article.author = request.user
            article.save()
            
            messages.success(request, f"Article '{article.title}' created successfully!")
            return redirect('news:detail', pk=article.pk)
    else:
        form = NewsForm()
    
    context = {
        'form': form,
        'title': 'Create News Article',
        'submit_text': 'Create Article',
    }
    return render(request, 'news/form.html', context)


@login_required
def edit_news(request, pk):
    if not is_teamleader(request.user):
        messages.error(request, "Only Team Leaders can edit news articles.")
        return redirect('news:detail', pk=pk)
    
    article = get_object_or_404(NewsArticle, pk=pk)
    
    if request.method == 'POST':
        form = NewsForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, f"Article '{article.title}' updated successfully!")
            return redirect('news:detail', pk=article.pk)
    else:
        form = NewsForm(instance=article)
    
    context = {
        'form': form,
        'article': article,
        'title': 'Edit News Article',
        'submit_text': 'Save Changes',
    }
    return render(request, 'news/form.html', context)


@login_required
def delete_news(request, pk):
    if not is_teamleader(request.user):
        messages.error(request, "Only Team Leaders can delete news articles.")
        return redirect('news:detail', pk=pk)
    
    article = get_object_or_404(NewsArticle, pk=pk)
    
    if request.method == 'POST':
        article_title = article.title
        article.delete()
        messages.success(request, f"Article '{article_title}' has been deleted.")
        return redirect('news:index')
    
    context = {
        'article': article,
    }
    return render(request, 'news/confirm_delete.html', context)
