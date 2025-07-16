# gunicorn.conf.py
workers = 4
worker_class = 'gevent'  # Use gevent for async support
timeout = 120  # Increase timeout to handle long-running SSE connections
bind = '0.0.0.0:5000'
loglevel = 'info'
accesslog = '-'  # Log to stdout
errorlog = '-'   # Log to stdout
