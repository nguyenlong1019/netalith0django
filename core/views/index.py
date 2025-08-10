from django.shortcuts import render 
from django.contrib.auth.decorators import login_required
from django.db.models import F
from core.models.assistant import AssistantLog 
from core.models.feed import Feed 


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
    pass 


def feed_category_view(request, categpry = None):
    pass 


def feed_detail_view(request, category = None, title_slug = None):
    pass 


def post_view(request):
    pass 


def post_category_view(request, categpry = None):
    pass 


def post_detail_view(request, category = None, title_slug = None):
    pass 