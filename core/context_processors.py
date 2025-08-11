from django.conf import settings

def default(request):
    dashboard_route = f'/{settings.ADMIN_ROUTE}/' if settings.ADMIN_ROUTE else '/admin/'
    random_images = [
        'https://flowbite.s3.amazonaws.com/blocks/marketing-ui/article/blog-1.png',
        'https://flowbite.s3.amazonaws.com/blocks/marketing-ui/article/blog-2.png',
        'https://flowbite.s3.amazonaws.com/blocks/marketing-ui/article/blog-3.png',
        'https://flowbite.s3.amazonaws.com/blocks/marketing-ui/article/blog-4.png'
    ]
    return {
        'dashboard_route': dashboard_route,
        'random_images': random_images
    }