"""
WSGI config for saip project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

#import os
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gdt_project.settings")

#from django.core.wsgi import get_wsgi_application
#application = get_wsgi_application()

# -.- coding: utf-8 -.-
import os, sys
from app import settings
 
path = settings.PATH
if path not in sys.path:
    sys.path.append(path)
 
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
 
from django.core.wsgi import get_wsgi_application
_application = get_wsgi_application()
