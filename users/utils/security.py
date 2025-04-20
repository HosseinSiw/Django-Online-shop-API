from django.core.cache import cache

BLOCK_TIME_SECONDS = 60 * 5 # 5 minuts
MAX_FAILED_ATTEMPS = 5

def get_ip_from_request(request):
    x_forwared_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwared_for:
        ip = x_forwared_for.split(',')[0].strip()
    else:
        ip = request.META.get("REMOTE_ADDR")
    
    return ip

def track_login_failure(ip):
    key = f'failed_attemps:{ip}'
    attemps = cache.get(key, 0) + 1
    cache.set(key, attemps, timeout=BLOCK_TIME_SECONDS)
    
    if attemps >= MAX_FAILED_ATTEMPS:
        cache.set(f"blocked_ip{ip}", True, timeout=BLOCK_TIME_SECONDS)
        cache.delete(key)

def reset_login_attemps(ip):
    key = f'failed_attemps:{ip}'
    cache.delete(key)
    