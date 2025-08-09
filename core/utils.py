import jwt, uuid, datetime 
from django.conf import settings 
from core.models.user import User 
from itsdangerous import URLSafeTimedSerializer


def _now_utc():
    return datetime.datetime.utcnow()


def _exp(ttl):
    return _now_utc() + ttl


def encode_access(user, extra=None):
    payload = {
        "sub": str(user.id),
        "type": "access",
        "iat": int(_now_utc().timestamp()),
        "exp": int(_exp(settings.JWT_ACCESS_TTL).timestamp()),
        "jti": uuid.uuid4().hex,
        "username": user.email,
    }
    if extra: payload.update(extra)
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALG)


def encode_refresh(user, extra=None):
    payload = {
        "sub": str(user.id),
        "type": "refresh",
        "iat": int(_now_utc().timestamp()),
        "exp": int(_exp(settings.JWT_REFRESH_TTL).timestamp()),
        "jti": uuid.uuid4().hex,
    }
    if extra: payload.update(extra)
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALG)


def decode_token(raw):
    return jwt.decode(raw, settings.JWT_SECRET, algorithms=[settings.JWT_ALG])


def get_user(sub):
    try:
        return User.objects.get(pk=sub)
    except User.DoesNotExist:
        return None


def generate_verification_token(email):
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    return serializer.dumps(email, salt='email-verify')


def verify_token(token):
    max_age = 5*60 if settings.DB_MODE == 'development' else 24*3600
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    try:
        email = serializer.loads(token, salt='email-verify', max_age=max_age)
        return email 
    except Exception as e:
        return False 
