#!/usr/bin/env python
import sys
import re
from format import *
from get_text import get_text

def kwic(results, path, q, byte_query, start, end, length=400):
    kwic_results = []
    shortest_biblio = 0
    for hit in results[start:end]:
        biblio = hit.author + ', ' +  hit.title
        get_query = byte_query(hit.bytes)
        href = "./" + '/'.join([str(i) for i in hit.philo_id[:5]]) + get_query
        
        ## Find shortest bibliography entry
        biblio = biblio
        if shortest_biblio == 0:
            shortest_biblio = len(biblio)
        if len(biblio) < shortest_biblio:
            shortest_biblio = len(biblio)
            
        ## Get concordance and align it
        bytes, byte_start = adjust_bytes(hit.bytes, length)
        conc_text = get_text(hit, byte_start, length, path)
        conc_start, conc_middle, conc_end = chunkifier(conc_text, bytes, highlight=True, kwic=True)
        conc_start = clean_text(conc_start, kwic=True)
        conc_end = clean_text(conc_end, kwic=True)
        conc_middle = clean_text(conc_middle, notag=False, kwic=True)
        conc_text = (conc_start + conc_middle + conc_end).decode('utf-8', 'ignore')
        conc_text = align_text(conc_text, len(hit.bytes))
        kwic_results.append((biblio, href, conc_text, hit))
    
    ## Populate Kwic_results with bibliography    
    for pos, result in enumerate(kwic_results):
        biblio, href, text, hit = result
        biblio = biblio[:shortest_biblio]
        biblio = '<a href="%s">' % href + biblio + '</a>: '
        kwic_results[pos] = (biblio + text, hit)
    return kwic_results