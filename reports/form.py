#!/usr/bin/env python

import sys
sys.path.append('..')
from functions.wsgi_handler import wsgi_response
from render_template import render_template


def form(start_response, environ):
    db, dbname, path_components, q = wsgi_response(start_response, environ)
    return render_template(db=db,dbname=dbname,form=True, template_name='form.mako')
