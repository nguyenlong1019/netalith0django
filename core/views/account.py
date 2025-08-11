from django.shortcuts import render, redirect 
from django.contrib import messages 
from django.contrib.auth import login, logout, authenticate 
from django.contrib.auth.decorators import login_required 
from core.models.user import User 
from django.contrib.auth.models import Group 
from django.http import FileResponse, Http404, JsonResponse, HttpResponse 
import mimetypes 
from core.utils import * 
from core.cookies import cookie_kwargs 
from django.conf import settings 
import json 
import os 
import sys 
import subprocess
from urllib.parse import urlencode 
from django.template.loader import render_to_string 
from utils.utils import is_valid_email 
from decouple import config 
from core.models.feed import Feed 


ACCESS_COOKIE = "access_token"
REFRESH_COOKIE = "refresh_token"

MAX_AGE_ACCESS =  int(config('MAX_AGE_ACCESS')) if config('MAX_AGE_ACCESS') else 2*3600
MAX_AGE_REFRESH = int(config('MAX_AGE_REFRESH')) if config('MAX_AGE_REFRESH') else 60*24*3600
 

def login_view(request):
    if request.user.is_authenticated:
        return redirect('index_view')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if not email or not password:
            messages.error(request, 'Please enter both email and password!')
            return redirect('login_view')
        user = authenticate(request, email=email, password=password)
        if not user:
            messages.error(request, "Email or password incorrect!")
            return redirect('login_view')

        if not user.is_verified:
            messages.info(request, "Please check email end click verify button to take the next step!")
            return redirect('login_view') 

        login(request, user)

        access = encode_access(user, extra = {'role': 'user'})
        refresh = encode_refresh(user)

        # print(access)
        # print(refresh)

        resp = redirect(request.GET.get('next') or 'index_view')
        resp.set_cookie(ACCESS_COOKIE, access, **cookie_kwargs(request, max_age=MAX_AGE_ACCESS))
        resp.set_cookie(REFRESH_COOKIE, refresh, **cookie_kwargs(request, max_age=MAX_AGE_REFRESH))
        return resp

    return render(request, 'core/login.html', status=200)


def register_view(request):
    if request.user.is_authenticated:
        return redirect('index_view')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')
        if not email or not password or not confirm_password:
            messages.error(request, 'Please enter email, password and confirm password!')
            return redirect('register_view')
        if password != confirm_password:
            messages.error(request, 'Password and confirm password does not match!')
            return redirect('register_view')
        if not is_valid_email(email):
            messages.error(request, "Email invalid!")
            return render(request, 'core/register.html', status=200) 
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!, Please use another email!.")
            return render(request, 'core/register.html', status=200) 
        user = User.objects.create_user(
            email=email,
            password=password,
            is_staff=True
        )
        
        user_group, created = Group.objects.get_or_create(name='User0Django')
        user.groups.add(user_group)

        # send email verify 
        script_path = os.path.join(settings.BASE_DIR, 'tasks', 'send_email.py')
        token = generate_verification_token(email)
        verification_url = request.build_absolute_uri(f"/verify-email?token={token}")
        template = 'email/register.html'
        html_body = render_to_string(template, {
            'email': email,
            'verify_url': verification_url
        })
        data = {
            'to': email,
            'from': settings.EMAIL_HOST_USER,
            'subject': 'Verify Account',
            'html_body': html_body
        }
        process = subprocess.Popen(
            [sys.executable, script_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        ).stdin.write(json.dumps(data))
        msg = 'Register successfully, please close this window and check your email to verify account!'
        return HttpResponse(f'<h1>{msg}</h1>')
        # login(request, user)
        # return redirect('index_view')
    return render(request, 'core/register.html', status=200)


@login_required(login_url='/login')
def logout_view(request):
    resp = redirect('index_view')
    resp.delete_cookie(ACCESS_COOKIE)
    resp.delete_cookie(REFRESH_COOKIE)
    logout(request)  # clear session
    return resp


@login_required(login_url='/login')
def my_profile_view(request):
    # f = request.user.profile_file 
    # if f and f.name.lower().endswith(('.html', '.htm')):
    #     try:
    #         fileobj = f.open('rb')
    #     except Exception:
    #         raise Http404("Profile file not found")
    #     content_type, _ = mimetypes.guess_type(f.name)
    #     if not content_type:
    #         content_type = 'text/html'
    #     resp = FileResponse(fileobj, content_type=content_type)
    #     return render(request, request.user.profile_file, status=200)
    feeds = Feed.objects.filter(type='feed', author=request.user).order_by('-created_at')
    posts = Feed.objects.filter(type='academic', author=request.user).order_by('-created_at')
    context = {}
    context['feeds'] = feeds[:4]
    context['posts'] = posts[:4] 
    return render(request, 'core/my-profile.html', context, status=200)


from django.views.decorators.http import require_POST 
@require_POST
def refresh_token_view(request):
    # print("Refresh token...")
    raw = request.COOKIES.get(REFRESH_COOKIE)
    if not raw:
        return JsonResponse({
            'msg': '',
            'error': 'Missing refresh token'
        }, status=401)
    try:
        payload = decode_token(raw)
        if payload.get('type') != 'refresh':
            return JsonResponse({
                'msg': '',
                'error': 'Invalid token type'
            }, status=401)
        user = get_user(payload.get("sub"))
        if not user:
            return JsonResponse({
                'msg': '',
                'error': 'User not found'
            }, status=401)
        new_access = encode_access(user)
        new_refresh = encode_refresh(user)
        resp = JsonResponse({
            'msg': 'Refreshed',
            'error': ''
        }, status=200)
        resp.set_cookie(ACCESS_COOKIE, new_access, **cookie_kwargs(request, max_age=MAX_AGE_ACCESS))
        resp.set_cookie(REFRESH_COOKIE, new_refresh, **cookie_kwargs(request, max_age=MAX_AGE_REFRESH))
        return resp 
    except Exception as e:
        return JsonResponse({
            'msg': '',
            'error': 'Invalid/expired refresh'
        }, status=401) 
    

def verify_email_view(request):
    token = request.GET.get('token')
    email = verify_token(token)
    if not email:
        return HttpResponse("<h1>Link expired or invalid</h1>", status=200)
    try:
        user = User.objects.get(email=email)
        if user.is_verified:
            return redirect('index_view')
        user.is_verified = True
        user.save()
        login(request, user)
        return redirect('index_view')
    except Exception as e:
        return HttpResponse(f"<p>Error: {str(e)}</p>", status=200)
