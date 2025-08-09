from functools import wraps 
from django.http import JsonResponse, HttpResponseRedirect 
from django.urls import reverse 
from core.utils import decode_token, get_user 


ACCESS_TOKEN = "access_token"


def oauth_required(view_func, *, api = True):
    """
    api=True -> 401 invalid
    api=False -> redirect login 
    """
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        print(f"cookies:{request.COOKIES}")
        raw = request.COOKIES.get(ACCESS_TOKEN)
        print(f"raw:{raw}")
        if not raw:
            return JsonResponse({
                'msg': '',
                'error': 'Unauthorized'
            }, status=401) if api else HttpResponseRedirect(reverse('login_view'))
        try:
            payload = decode_token(raw)
            if payload.get('type') != 'access':
                raise ValueError("wrong token type")
            user = get_user(payload.get('sub'))
            if not user:
                raise ValueError("user not found")
            request.oauth_user = user 
            request.jwt_payload = payload 
        except Exception as e:
            return JsonResponse({
                'msg': '',
                'error': f'{str(e)}'
            }, status=401) if api else HttpResponseRedirect(reverse("login_view"))

        return view_func(request, *args, **kwargs)
    return _wrapped
        