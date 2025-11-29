import secrets
def slugify():
    return secrets.token_urlsafe(12)
