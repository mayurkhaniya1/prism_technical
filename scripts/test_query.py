import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','taskmanager.settings')
import django
django.setup()
from api.models import Issue
from django.contrib.auth.models import User
try:
    u = User.objects.get(username='testuser')
    count = Issue.objects.filter(project__organization__memberships__user=u).count()
    print('OK, query executed, count =', count)
except Exception as e:
    print('ERROR', repr(e))
