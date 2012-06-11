from __future__ import division
import sys
sys.path.append('..')
import functions as f
import os
import re
from functions.wsgi_handler import wsgi_response
from bibliography import bibliography
from render_template import render_template
from concordance import fetch_concordance

def theme_rheme(start_response, environ):
    db, dbname, path_components, q = wsgi_response(start_response, environ)
    path = os.getcwd().replace('functions/', '')
    if q['q'] == '':
        return bibliography(f,path, db, dbname,q,environ)
    else:
        hits = db.query(q["q"],q["method"],q["arg"],**q["metadata"])
        new_hits = adjust_results(hits, path, q)
        return render_template(results=new_hits,db=db,dbname=dbname,q=q,fetch_concordance=fetch_concordance,f=f,
                                path=path, results_per_page=q['results_per_page'], template_name="theme_rheme.mako")
                                
def adjust_results(hits, path, q):
    front_of_clause = 35
    end_of_clause = 90
    length = 600 ## pull 600 bytes for concordance: maybe adjust dynamically?
    word = q['q']
    punctuation = re.compile('([,|?|;|.|:|!])')
    new_results = []
    for hit in hits:
        bytes, byte_start = f.format.adjust_bytes(hit.bytes, length)
        conc_text = f.get_text(hit, byte_start, length, path)
        conc_start = conc_text[:bytes[0]]
        clause_start = punctuation.split(conc_start)[-1] # keep only last bit
        conc_end = conc_text[bytes[0]:]
        clause_end = punctuation.split(conc_end)[0] # keep only first bit
        clause = f.format.clean_text(clause_start + clause_end)
        new_clause = [i for i in clause.split() if len(i) > 2 or i.lower() == word]
        if len(new_clause) < 3:
            continue
        word_position = 0
        for pos, w in enumerate(new_clause):
            if w.lower() == word:
                word_position = pos + 1
                break
        clause_len = len(new_clause)
        percentage = round(word_position / clause_len * 100, 2)
        if q['theme_rheme'] == 'front' and percentage <= front_of_clause:
            hit.percentage = str(percentage) + '%'
            hit.position = str(word_position) + '/' + str(clause_len)
            new_results.append(hit)
        elif q['theme_rheme'] == 'end' and percentage >= end_of_clause:
            hit.percentage = str(percentage) + '%'
            hit.position = str(word_position) + '/' + str(clause_len)
            new_results.append(hit)
    return new_results
    
    