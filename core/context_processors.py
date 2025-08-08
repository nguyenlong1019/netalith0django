from django.conf import settings

def default(request):
    dashboard_route = f'/{settings.ADMIN_ROUTE}/' if settings.ADMIN_ROUTE else '/admin/'
    return {
        'dashboard_route': dashboard_route
    }