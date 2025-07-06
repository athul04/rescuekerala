
release: python manage.py migrate
web: gunicorn floodrelief.wsgi --timeout 600	
worker: python redis_worker.py
