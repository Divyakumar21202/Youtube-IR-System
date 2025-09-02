from slowapi import Limiter
from slowapi.util import get_remote_address

# Identify users: fallback to IP if X-User-ID header not present
def get_user_key(request):
    return request.headers.get("X-User-ID") or get_remote_address(request)

# Limiter instance (in-memory, single-server)
limiter = Limiter(key_func=get_user_key)
