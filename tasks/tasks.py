from core.models.user import User 


def clear_user_not_verified():
    users = User.objects.filter(is_verified=False).exclude(is_superuser=True).delete()
    print("Success!")
