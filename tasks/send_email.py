import sys 
import json 
import os 
from decouple import config 


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "netalith0django.settings")
import django
django.setup()

from django.core.mail import EmailMessage
from core.models.log import EmailLog 
EMAIL_HOST_USER = config('EMAIL_HOST_USER')


def main():
    try:
        raw_input = sys.stdin.read()
        data = json.loads(raw_input)
        email = EmailMessage(
            subject=data.get("subject", "Test"),
            body=data.get("html_body", ""),  # HTML body
            from_email=data.get("from") or EMAIL_HOST_USER,
            to=[data.get("to")],
        )
        email.content_subtype = "html"
        if data.get('attachment_file_path'):
            email.attach_file(data.get('attachment_file_path'))
        email.send(fail_silently=False)
    except Exception as e:
        EmailLog.objects.create(
            data=data,
            error=str(e),
            order_id=data.get('order_id'),
            user_email=data.get('to')
        )
        sys.exit(1)


if __name__ == "__main__":
    main()