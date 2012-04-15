#!/usr/bin/env python

from mako.template import Template
from mako.lookup import TemplateLookup

## For debugging templates only ###
from mako import exceptions
###################################

def bibliography(HitWrapper, q, db, dbname, mytemplates):
    if q["no_q"]:
            hits = db.toms.get_documents()
    else:
        hits = db.toms.query(**q["metadata"])
    results = HitWrapper.metadata_results_wrapper(hits, db)
    template = Template(filename="templates/bibliography.mako", lookup=mytemplates)
    try:
        return template.render(results=results,db=db,dbname=dbname,q=q).encode("UTF-8", "ignore")
    except:
        return exceptions.html_error_template().render()