from django.conf import settings


def cookie_kwargs(request=None, max_age=None):
    return dict(
        httponly=True,
        secure=False if settings.DB_MODE == 'development' else True,
        samesite='Lax' if settings.DB_MODE == 'development' else 'Strict',
        path="/",
        max_age=max_age,
    )