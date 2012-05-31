#!/usr/bin/env python

import sys
sys.path.append('..')
import functions as f
import os
from functions.format import adjust_bytes, chunkifier, clean_text
from functions.wsgi_handler import wsgi_response
from get_text import get_text
from bibliography import bibliography
from render_template import render_template

def concordance(start_response, environ):
    db, dbname, path_components, q = wsgi_response(start_response, environ)
    path = os.getcwd().replace('functions/', '')
    if q['q'] == '':
        return bibliography(f,path, db, dbname,q,environ)
    else:
        hits = db.query(q["q"],q["method"],q["arg"],**q["metadata"])
        return render_template(results=hits,db=db,dbname=dbname,q=q,fetch_concordance=fetch_concordance,f=f,
                                path=path, results_per_page=q['results_per_page'], template_name="concordance.mako")

def fetch_concordance(hit, path, q, length=400):
    bytes, byte_start = f.format.adjust_bytes(hit.bytes, length)
    conc_text = get_text(hit, byte_start, length, path)
    conc_start, conc_middle, conc_end = f.format.chunkifier(conc_text, bytes, highlight=True)
    conc_start = f.format.clean_text(conc_start)
    conc_end = f.format.clean_text(conc_end)
    conc_text = conc_start + conc_middle + conc_end
    return conc_text.decode('utf-8', 'ignore')
    
