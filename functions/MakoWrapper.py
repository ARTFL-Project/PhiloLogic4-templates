#!/usr/bin env python

from mako.template import Template
from mako.lookup import TemplateLookup
from mako import exceptions

def render_template(*args, **data):
    db = data["db"]
    templates = TemplateLookup(db.locals['db_path'].replace('data', ''))  ##  the replace is a workaround for something I need to change in the Loader class
    template = Template(filename="templates/%s" % data['template_name'], lookup=templates)
    if not db.locals['debug']:
        return template.render(*args, **data).encode("UTF-8", "ignore")
    else:
        try:
            return template.render(*args, **data).encode("UTF-8", "ignore")
        except:
            return exceptions.html_error_template().render()