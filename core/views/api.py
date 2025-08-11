from django.contrib.auth.decorators import login_required
from django.http import JsonResponse 
from django.views.decorators.http import require_POST
from core.decorators import oauth_required
from core.service import ChatGPTService
import json 


# @login_required(login_url='login')
# @require_POST
@oauth_required
def ai_ask_api(request):
    if not request.user.is_authenticated:
        return JsonResponse({
            'msg': '',
            'error': 'Login required!',
            'status': 400,
            'code': 2,
            'reply': {}
        })
    if request.method == 'POST':
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
        c = ChatGPTService(user_id=request.user.id)
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
        return JsonResponse({
            'msg': 'ok',
            'error': result,
            'status': 200,
            'code': 0,
            'reply': result
        }, status=200)


from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.db.models import F
from django.shortcuts import get_object_or_404
from django.utils.html import strip_tags
from core.models.feed import Feed, FeedComment, FeedReaction, REACTION_CHOICES

REACTION_TYPES = {str(k): v for k, v in REACTION_CHOICES}  # {"1":"like","2":"heart"}


def react_feed(request, feed_id):
    feed = get_object_or_404(Feed, pk=feed_id, status__in=[0,1])  # cho phép draft/published nếu bạn muốn

    rtype = request.POST.get("type")  # "1" (like) | "2" (heart)
    if rtype not in REACTION_TYPES:
        return HttpResponseBadRequest("Invalid reaction type")

    try:
        obj = FeedReaction.objects.get(user=request.user, feed=feed)
        if str(obj.type) == rtype:
            # cùng loại -> unreact
            obj.delete()
            Feed.objects.filter(pk=feed.pk).update(total_react=F("total_react") - 1)
            action = "unreacted"
        else:
            # đổi loại -> giữ total_react
            obj.type = int(rtype)
            obj.save(update_fields=["type"])
            action = "switched"
    except FeedReaction.DoesNotExist:
        # chưa có -> tạo mới
        FeedReaction.objects.create(user=request.user, feed=feed, type=int(rtype))
        Feed.objects.filter(pk=feed.pk).update(total_react=F("total_react") + 1)
        action = "reacted"

    # (tuỳ chọn) đếm theo loại, nếu bạn muốn hiển thị
    counts = FeedReaction.objects.filter(feed=feed).values("type").order_by().annotate(c=models.Count("type"))
    by_type = {item["type"]: item["c"] for item in counts}

    feed.refresh_from_db(fields=["total_react"])
    return JsonResponse({
        "ok": True,
        "action": action,           # reacted | unreacted | switched
        "total_react": feed.total_react,
        "like_count": by_type.get(1, 0),
        "heart_count": by_type.get(2, 0),
    })


def comment_feed(request, feed_id):
    feed = get_object_or_404(Feed, pk=feed_id, status__in=[0,1])
    content = request.POST.get("content", "").strip()
    # bảo vệ tối thiểu
    if not content or len(strip_tags(content)) < 2:
        return HttpResponseBadRequest("Empty content")

    cmt = FeedComment.objects.create(user=request.user, feed=feed, content=content)
    Feed.objects.filter(pk=feed.pk).update(total_comment=F("total_comment") + 1)

    # trả HTML đơn giản cho client chèn vào list (hoặc trả data để client tự render)
    return JsonResponse({
        "ok": True,
        "id": cmt.id,
        "user": str(request.user),
        "content": cmt.content,   # bạn đang dùng HTMLField
        "created_at": cmt.created_at.isoformat(),
    })