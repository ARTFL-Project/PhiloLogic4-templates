#!/usr/bin/env python
from mako.template import Template
from mako.lookup import TemplateLookup
from format import adjust_bytes, chunkifier, clean_text
from get_text import get_text
from bibliography import bibliography

## For debugging templates only ###
from mako import exceptions
###################################

def concordance(h, HitWrapper, IRHitWrapper, path, db, dbname, q, environ):
    mytemplates = TemplateLookup(path)
    if q['q'] == '':
        return bibliography(HitWrapper, q, db, dbname, mytemplates)
    else:
        hits = db.query(q["q"],q["method"],q["arg"],**q["metadata"])
        results = HitWrapper.results_wrapper(hits,db)
        template = Template(filename="templates/concordance.mako", lookup=mytemplates)
        try:
            return template.render(results=results,db=db,dbname=dbname,q=q,fetch_concordance=fetch_concordance,h=h,
                                    path=path, results_per_page=q['results_per_page']).encode("UTF-8", "ignore")
        except:
            return exceptions.html_error_template().render()

def fetch_concordance(hit, path, q, length=400):
    bytes, byte_start = adjust_bytes(hit.bytes, length)
    conc_text = get_text(hit, byte_start, length, path)
    conc_start, conc_middle, conc_end = chunkifier(conc_text, bytes, highlight=True)
    conc_start = clean_text(conc_start)
    conc_end = clean_text(conc_end)
    conc_text = conc_start + conc_middle + conc_end
    return conc_text.decode('utf-8', 'ignore')
    
