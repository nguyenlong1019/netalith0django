from django.utils.html import format_html 
from django.contrib.humanize.templatetags.humanize import intcomma 
import re 
from django.utils.timezone import localdate, localtime 
import requests 


def to_display_image_ext(url, desc):
    if url:
        return format_html('<a href="{}" target="_blank"><img src="{}" alt="{}" style="width: 40px;height: 40px;border-radius: 50%;border: 2px solid #fff;"/></a>', url, url, desc)
    return format_html('<img src="https://cdn-icons-png.flaticon.com/128/14534/14534501.png" alt="No image" style="width: 40px;height: 40px;border-radius: 50%;border: 2px solid #000;"/>', url, desc)


def to_display_image(url, desc):
    if url:
        return format_html('<img src="{}" alt="{}" style="width: 40px;height: 40px;border-radius: 50%;border: 2px solid #fff;"/>', url, desc)
    return format_html('<img src="/static/assets/images/noimage/no-picture-taking.png" alt="No image" style="width: 40px;height: 40px;border-radius: 50%;border: 2px solid #000;"/>', url, desc)


def to_blank_window(url, desc):
    return format_html('<a href="{}" target="_blank">{}</a>', url, desc)


def to_download_window(url, desc):
    return format_html('<a href="{}" download>{}</a>', url, desc)


def to_price_format(amount):
    try:
        return format_html("{} đ", intcomma(amount))
    except Exception:
        return "0 đ"
    

def is_valid_email(email):
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(regex, email) is not None


def to_localtime(time):
    try:
        return localtime(time).strftime("%d-%m-%Y %H:%M:%S")
    except Exception as e:
        return ''
    

def to_localdate(date):
    try:
        return localdate(date).strftime("%Y-%m-%d")
    except Exception as e:
        return ''


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')


def get_headers_dict(request):
    return {
        k: v for k, v in request.META.items()
        if k.startswith("HTTP_") or k in ['CONTENT_TYPE', 'CONTENT_LENGTH']
    }


def get_ip_info(ip):
    response = requests.get(f"https://ipwho.is/{ip}")
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            return {
                "ip": ip,
                "country": data.get("country"),
                "country_code": data.get("country_code"),
                "region": data.get("region"),
                "city": data.get("city"),
                "org": data.get("connection", {}).get("isp"),
                "data_json": data 
            }
    return None 