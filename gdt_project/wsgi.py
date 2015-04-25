"""
WSGI config for  gdt_project.
 
It exposes the WSGI callable as a module-level variable named ``application``.
 
For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""
 
import os# -.- coding: utf-8 -.-
import os, sys
from gdt_project import settings
path = settings.PATH
if path not in sys.path:
    sys.path.append(path)
 
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gdt_project.settings")
 
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
# -.- coding: utf-8 -.-
