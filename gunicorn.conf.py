# gunicorn.conf.py
workers = 4
worker_class = 'gevent'  # Use gevent for async support
timeout = 120  # Increased timeout for SSE
bind = '0.0.0.0:5000'
loglevel = 'info'
accesslog = '-'  # Log to stdout
errorlog = '-'   # Log to stdout
