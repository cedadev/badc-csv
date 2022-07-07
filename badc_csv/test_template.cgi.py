#!/usr/local/ceda_mezzanine/venv/bin/python
#
# How to get template to work from python cgi script
#

from django.conf import settings
import django.template.loader
from django.template import Template, Context
import django
import sys
import codecs

# minimal settings file                                                                                                             
settings.configure(TEMPLATES=[{'BACKEND': 'django.template.backends.django.DjangoTemplates','DIRS': [],
                              'APP_DIRS': True,'OPTIONS': {}}],
                   INSTALLED_APPS=['fwtheme_django_ceda_serv', 'fwtheme_django', 'django.contrib.staticfiles', 'cookielaw'],
                   STATIC_URL='/static')
django.setup()

# make a template that extends the base layout from the fwtheme layout. This replaces the content block with a content variable     

t = Template('{% extends "fwtheme_django/layout.html" %} {% block content_header %}{% endblock content_header %} {% block content %}{{content|safe}}{% endblock content %}')

content = """Normal CGI output (<bold>tags ok</bold>)"""

print("Content-type: text/html")
print("")
print("")

sys.stdout = codecs.getwriter('utf8')(sys.stdout)
print(t.render(Context({'content': content})))
