from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from fastapi import Request
from fastapi.responses import JSONResponse

#rate limit configuration
limiter = Limiter(key_func=get_remote_address)
async def rate_limit_handler(request: Request, exc:RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={
            "detail": "Too many requests",
            "limit": str(exc)
        }
    )

#predefined rate limits
#less tries for auth to prevent brute force
limit_auth = limiter.limit("5/minute")
#standard limit
limit_standard = limiter.limit("60/minute")
#lower limit for dashboard
limit_dashboard = limiter.limit("30/minute")
#less tries for admin operations
limit_admin_write = limiter.limit("20/minute")

def register_rate_limiter(app):
    app.state.limiter= limiter
    app.add_exception_handler(RateLimitExceeded, rate_limit_handler)
    app.add_middleware(SlowAPIMiddleware)
