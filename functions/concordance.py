#!/usr/bin/env python
from format import adjust_bytes, chunkifier, clean_text
from get_text import get_text
from bibliography import bibliography
from MakoWrapper import render_template
import sys

def concordance(h, path, path_components, db, dbname, q, environ):
    if q['q'] == '':
        return bibliography(h,path,path_components, db, dbname,q,environ)
    else:
        hits = db.query(q["q"],q["method"],q["arg"],**q["metadata"])
        return render_template(results=hits,db=db,dbname=dbname,q=q,fetch_concordance=fetch_concordance,h=h,
                                path=path, results_per_page=q['results_per_page'], template_name="concordance.mako")

def fetch_concordance(hit, path, q, length=400):
    bytes, byte_start = adjust_bytes(hit.bytes, length)
    conc_text = get_text(hit, byte_start, length, path)
    conc_start, conc_middle, conc_end = chunkifier(conc_text, bytes, highlight=True)
    conc_start = clean_text(conc_start)
    conc_end = clean_text(conc_end)
    conc_text = conc_start + conc_middle + conc_end
    return conc_text.decode('utf-8', 'ignore')
    
