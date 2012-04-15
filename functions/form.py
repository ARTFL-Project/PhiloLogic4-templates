#!/usr/bin/env python
from mako.template import Template
from mako.lookup import TemplateLookup
import os
import sys

def form(h, path, path_components, db, dbname, q, environ):
    mytemplates = TemplateLookup(path)
    template = Template(filename="templates/form.mako", lookup=mytemplates)
    path_components = [c for c in environ["PATH_INFO"].split("/") if c]
    return template.render(db=db,dbname=dbname,form=True).encode("UTF-8")