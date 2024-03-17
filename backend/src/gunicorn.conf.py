import os

# server
bind = f'{os.getenv("API_GUNICORN_HOST", "0.0.0.0")}:{os.getenv("API_GUNICORN_PORT", 9081)}'

# workers
workers = os.getenv("API_GUNICORN_WORKERS", 2)
timeout = 120
preload_app = True

# development
reload = os.getenv("API_DEBUG_MODE", False)
