# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.logo = A(B('Scavi-Hunt'),XML('&trade;&nbsp;'),
                  _class="brand",_href="peter1123.pythonanywhere.com/ScaviHunt/default/index")
#"http://127.0.0.1:8000/ScaviHunt"

## response.title = request.application.replace('_',' ').title()
## response.subtitle = ''

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Your Name <you@example.com>'
response.meta.description = 'a cool new app'
response.meta.keywords = 'web2py, python, framework'
response.meta.generator = 'Web2py Web Framework'

## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################

response.menu = [
    ('Home', False, URL('default', 'index')),
    ('Hunt Admin', False, URL('default', 'hunt_admin')),
    ('User Admin', False, URL('default', 'user_admin'))]

##('Map', False, URL('default', 'googleMap'))

if False:
    auth.wikimenu()
