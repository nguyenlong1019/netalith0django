from django.conf import settings
from django.db.models import F, Sum, Q
from core.models.game import Game 
from core.models.user import User 
from core.models.category import Tag 


def default(request):
    dashboard_route = f'/{settings.ADMIN_ROUTE}/' if settings.ADMIN_ROUTE else '/admin/'
    random_images = [
        'https://flowbite.s3.amazonaws.com/blocks/marketing-ui/article/blog-1.png',
        'https://flowbite.s3.amazonaws.com/blocks/marketing-ui/article/blog-2.png',
        'https://flowbite.s3.amazonaws.com/blocks/marketing-ui/article/blog-3.png',
        'https://flowbite.s3.amazonaws.com/blocks/marketing-ui/article/blog-4.png'
    ]
    random_logo_games = [
        'https://picsum.photos/seed/1/48/48',
        'https://picsum.photos/seed/2/48/48',
        'https://picsum.photos/seed/3/48/48'
    ]

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
    return {
        'dashboard_route': dashboard_route,
        'random_images': random_images,
        'random_logo_games': random_logo_games,
        'game_hot': game_hot,
        'top_authors': top_authors_by_feed_interactions,
        'top_tags': top_tags_by_feed_interactions,
    }