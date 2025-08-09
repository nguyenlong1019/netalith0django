from django.contrib.auth.decorators import login_required
from django.http import JsonResponse 
from django.views.decorators.http import require_POST
from core.decorators import oauth_required
from core.service import ChatGPTService
import json 


@login_required(login_url='login')
@require_POST
@oauth_required
def ai_ask_api(request):
    data = json.loads(request.body)
    user_msg = data.get('user_msg')
    if not user_msg:
        return JsonResponse({
            'msg': '',
            'error': 'Please enter prompt!',
            'status': 400,
            'code': 1,
            'reply': {}
        }, status=400)
    c = ChatGPTService({'user_id': request.user.id})
    params = {'user_content': user_msg}
    is_success, result = c.run(params)
    if is_success:
        return JsonResponse({
            'msg': 'ok',
            'error': '',
            'status': 200,
            'code': 0,
            'reply': result
        }, status=200)
