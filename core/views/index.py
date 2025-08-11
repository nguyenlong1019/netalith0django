from django.shortcuts import render 
from django.contrib.auth.decorators import login_required
from django.db.models import F, Count, Sum, Q
from core.models.assistant import AssistantLog 
from core.models.feed import Feed 
from core.models.category import Category, Tag 
from core.models.user import User 
from core.models.game import Game 
from django.http import Http404, HttpResponseBadRequest


def index_view(request):
    latest = Feed.objects.filter(status=1).order_by('-created_at')
    top = Feed.objects.filter(status=1).annotate(
        total_rank_db=F('total_comment') + F('total_view') + F('total_react')
    ).order_by('-created_at').order_by('-total_rank_db')

    top_authors_by_feed_interactions = (
        User.objects
            .annotate(
                interactions=Sum(
                    F('feed__total_view') + F('feed__total_react') + F('feed__total_comment'),
                    filter=Q(feed__status=1)
                )
            )
            .order_by('-interactions')[:5]
    )

    top_tags_by_feed_interactions = (
        Tag.objects
            .annotate(
                feed_interactions=Sum(
                    F('feed__total_view') + F('feed__total_react') + F('feed__total_comment'),
                    filter=Q(feed__status=1)
                )
            )
            .order_by('-feed_interactions')[:10]
    )

    game_hot = Game.objects.filter(status=1).annotate(
        total_rank_db=F('view_count') + F('play_count')
    ).order_by('-created_at').order_by('-total_rank_db')

    context = {}
    context['latest'] = latest[:10]
    context['top'] = top[:10]
    context['top_authors'] = top_authors_by_feed_interactions
    context['top_tags'] = top_tags_by_feed_interactions
    context['game_hot'] = game_hot 
    return render(request, 'core/index.html', context, status=200)


@login_required(login_url='/login')
def ai_assistant_view(request):
    messages = AssistantLog.objects.filter(user=request.user).order_by('created_at')
    return render(request, 'core/ai-assistant.html', {'messages': messages}, status=200)


def feed_view(request):
    latest = Feed.objects.filter(type='feed', status=1).order_by('-created_at')
    top = Feed.objects.filter(type='feed', status=1).annotate(
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
        category = Category.objects.get(slug=category_slug, status=1)
    except Exception as e:
        return HttpResponseBadRequest(f"{str(e)}")
    latest = Feed.objects.filter(type='feed', status=1).filter(category=category).order_by('-created_at')
    top = Feed.objects.filter(type='feed', status=1).filter(category=category).annotate(
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
        feed = Feed.objects.filter(type='feed', status=1).filter(category=category, slug=title_slug)
    except Exception as e:
        return HttpResponseBadRequest(f"{str(e)}")
    context = {}
    context['category'] = category 
    context['feed'] = feed 
    return render(request, 'core/feed_detail.html', context, status=200)


def post_view(request):
    latest = Feed.objects.filter(type='academic', status=1).order_by('-created_at')
    top = Feed.objects.filter(type='academic', status=1).annotate(
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
        category = Category.objects.get(slug=category_slug, status=1)
    except Exception as e:
        return HttpResponseBadRequest(f"{str(e)}") 
    latest = Feed.objects.filter(type='academic', status=1).filter(category=category).order_by('-created_at')
    top = Feed.objects.filter(type='academic', status=1).filter(category=category).annotate(
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
        feed = Feed.objects.filter(type='academic', status=1).filter(category=category, slug=title_slug)
    except Exception as e:
        return HttpResponseBadRequest(f"{str(e)}") 
    context = {}
    context['category'] = category 
    context['feed'] = feed 
    return render(request, 'core/post_detail.html', context, status=200)


def author_profile_view(request, nickname = None):
    if not nickname:
        return Http404('<h1>404 Not Found</h1>')
    try:
        author = User.objects.get(nickname=nickname)
    except Exception as e:
        author = False 
    try:
        author = User.objects.get(email=nickname)
    except Exception as e:
        author = False 
    if not author:
        return Http404('<h1>404 Not Found</h1>')
    feeds = Feed.objects.filter(type='feed', author=author, status=1).order_by('-created_at')
    posts = Feed.objects.filter(type='academic', author=author, status=1).order_by('-created_at')
    context = {}
    context['author'] = author 
    context['feeds'] = feeds[:4]
    context['posts'] = posts[:4]
    return render(request, 'core/author.html', context, status=200)


def author_feed_view(request, nickname = None):
    if not nickname:
        return Http404('<h1>404 Not Found</h1>')
    try:
        author = User.objects.get(nickname=nickname)
    except Exception as e:
        author = False 
    try:
        author = User.objects.get(email=nickname)
    except Exception as e:
        author = False 
    if not author:
        return Http404('<h1>404 Not Found</h1>')
    feeds = Feed.objects.filter(type='feed', author=author, status=1).order_by('-created_at')
    context = {}
    context['author'] = author 
    context['feeds'] = feeds
    return render(request, 'core/feed_by_author.html', context, status=200)


def author_post_view(request, nickname = None):
    if not nickname:
        return Http404('<h1>404 Not Found</h1>')
    try:
        author = User.objects.get(nickname=nickname)
    except Exception as e:
        author = False 
    try:
        author = User.objects.get(email=nickname)
    except Exception as e:
        author = False 
    if not author:
        return Http404('<h1>404 Not Found</h1>') 
    feeds = Feed.objects.filter(type='academic', author=author, status=1).order_by('-created_at')
    context = {}
    context['author'] = author
    context['feeds'] = feeds 
    return render(request, 'core/post_by_author.html', context, status=200)


def feed_by_tag_view(request, hash_name = None):
    if not hash_name:
        return Http404('<h1>404 Not Found</h1>')
    try:
        tag = Tag.objects.get(hash_name=hash_name)
    except Exception as e:
        tag = False 
    if not tag:
        return Http404('<h1>404 Not Found</h1>')
    feeds = Feed.objects.filter(status=1, tags=tag).order_by('-created_at')
    context = {}
    context['tag'] = tag 
    context['feeds'] = feeds 
    return render(request, 'core/feed_by_tag.html', context, status=200)


def game_view(request, game_slug = None):
    if not game_slug:
        return Http404('<h1>404 Not Found</h1>')
    try:
        game = Game.objects.get(slug=game_slug, status=1)
    except Exception as e:
        game = False 
    context = {}
    context['game'] = game 
    return render(request, 'core/game.html', context, status=200)


# http://127.0.0.1:8000/feed/tech-discuss/qa-how-to-embed-an-html5-game-in-0django