from django.shortcuts import render 
from django.contrib.auth.decorators import login_required
from django.db.models import F
from core.models.assistant import AssistantLog 
from core.models.feed import Feed 
from core.models.category import Category, Tag 
from django.http import Http404, HttpResponseBadRequest


def index_view(request):
    latest = Feed.objects.order_by('-created_at')
    top = Feed.objects.annotate(
        total_rank_db=F('total_comment') + F('total_view') + F('total_react')
    ).order_by('-created_at').order_by('-total_rank_db')
    context = {}
    context['latest'] = latest[:10]
    context['top'] = top[:10]
    return render(request, 'core/index.html', context, status=200)


@login_required(login_url='/login')
def ai_assistant_view(request):
    messages = AssistantLog.objects.filter(user=request.user).order_by('created_at')
    return render(request, 'core/ai-assistant.html', {'messages': messages}, status=200)


def feed_view(request):
    latest = Feed.objects.filter(type='feed').order_by('-created_at')
    top = Feed.objects.filter(type='feed').annotate(
        total_rank_db=F('total_comment') + F('total_view') + F('total_react')
    ).order_by('-created_at').order_by('-total_rank_db')
    context = {}
    context['latest'] = latest[:10]
    context['top'] = top[:10]
    return render(request, 'core/feed.html', context, status=200)


def feed_category_view(request, category_slug = None):
    if not category_slug:
        return Http404('<h1>404 Not Found</h1>')
    try:
        category = Category.objects.get(slug=category_slug)
    except Exception as e:
        return HttpResponseBadRequest(f"{str(e)}")
    latest = Feed.objects.filter(type='feed').filter(category=category).order_by('-created_at')
    top = Feed.objects.filter(type='feed').filter(category=category).annotate(
        total_rank_db=F('total_comment') + F('total_view') + F('total_react')
    ).order_by('-created_at').order_by('-total_rank_db')
    context = {}
    context['category'] = category 
    context['latest'] = latest[:10]
    context['top'] = top[:10]
    return render(request, 'core/feed_category.html', context, status=200)


def feed_detail_view(request, category_slug = None, title_slug = None):
    if not category_slug or not title_slug:
        return Http404('<h1>404 Not Found</h1>')
    try:
        category = Category.objects.get(slug=category_slug)
    except Exception as e:
        return HttpResponseBadRequest(f"{str(e)}")
    try:
        feed = Feed.objects.filter(type='feed').filter(category=category, slug=title_slug)
    except Exception as e:
        return HttpResponseBadRequest(f"{str(e)}")
    context = {}
    context['category'] = category 
    context['feed'] = feed 
    return render(request, 'core/feed_detail.html', context, status=200)


def post_view(request):
    latest = Feed.objects.filter(type='academic').order_by('-created_at')
    top = Feed.objects.filter(type='academic').annotate(
        total_rank_db=F('total_comment') + F('total_view') + F('total_react')
    ).order_by('-created_at').order_by('-total_rank_db')
    context = {}
    context['latest'] = latest[:10]
    context['top'] = top[:10]
    return render(request, 'core/post.html', context, status=200) 


def post_category_view(request, category_slug = None):
    if not category_slug:
        return Http404('<h1>404 Not Found</h1>')
    try:
        category = Category.objects.get(slug=category_slug)
    except Exception as e:
        return HttpResponseBadRequest(f"{str(e)}") 
    latest = Feed.objects.filter(type='academic').filter(category=category).order_by('-created_at')
    top = Feed.objects.filter(type='academic').filter(category=category).annotate(
        total_rank_db=F('total_comment') + F('total_view') + F('total_react')
    ).order_by('-created_at').order_by('-total_rank_db')
    context = {}
    context['category'] = category 
    context['latest'] = latest[:10]
    context['top'] = top[:10]
    return render(request, 'core/post_category.html', context, status=200)


def post_detail_view(request, category_slug = None, title_slug = None):
    if not category_slug or not title_slug:
        return Http404('<h1>404 Not Found</h1>')
    try:
        category = Category.objects.get(slug=category_slug)
    except Exception as e:
        return HttpResponseBadRequest(f"{str(e)}")
    try:
        feed = Feed.objects.filter(type='academic').filter(category=category, slug=title_slug)
    except Exception as e:
        return HttpResponseBadRequest(f"{str(e)}") 
    context = {}
    context['category'] = category 
    context['feed'] = feed 
    return render(request, 'core/post_detail.html', context, status=200)
