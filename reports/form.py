#!/usr/bin/env python
from render_template import render_template

def form(path, path_components, db, dbname, q, environ):
    path_components = [c for c in environ["PATH_INFO"].split("/") if c]
    return render_template(db=db,dbname=dbname,form=True, template_name='form.mako')
