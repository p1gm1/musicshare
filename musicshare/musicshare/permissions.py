def is_authenticated(user, **kwargs) -> bool:
    return user.is_authenticated

def is_admin(user, **kwargs) -> bool:
    return user.is_superuser
