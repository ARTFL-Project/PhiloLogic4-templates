#!/usr/bin/env python

import os
import sys
import cgi
import re
import urlparse ## to be removed when parse_cgi is moved elsewhere
from philologic.PhiloDB import PhiloDB
from crapser import crapser

## This function (without mods) already exists in philo_helpers.py: we need a helpers script
def parse_cgi(q, dbfile):
    cgi = urlparse.parse_qs(q,keep_blank_values=True)
    db = PhiloDB(dbfile)
    query = {}
    query["q"] = cgi.get("q",[None])[0]
    query["method"] = cgi.get("method",[None])[0] 
    query["arg"] = cgi.get("arg",[0])[0]
    query["report"] = cgi.get("report",[None])[0]
    query["format"] = cgi.get("format",[None])[0]
    query["results_per_page"] = int(cgi.get("results_per_page",[20])[0])
    
    ## Hack so that even if there are multiple byte offsets
    ## we still have it stored as a string in query
    query["byte"] = '+'.join(cgi.get("byte",['']))
    
    ## This defines within how many words for collocation tables
    query["word_num"] = int(cgi.get("word_num",[0])[0])
    
#    query["dbname"] = dbname
    query["dbpath"] = dbfile
    query["start"] = int(cgi.get('start',[0])[0]) # special range handling done in each service now.
    query["end"] = int(cgi.get('end',[0])[0]) 
    query["width"] = int(cgi.get("width",[0])[0]) or db.locals["conc_width"] # TODO: REMOVE
    query["field"] = cgi.get("field",[None])[0]
    query["metadata"] = {}
    metadata_fields = db.locals["metadata_fields"]
    num_empty = 0
    for field in metadata_fields:
        if field in cgi and cgi[field]:
            ## these ifs are to fix the no results you get when you do a metadata query
            if query["q"] != '':
                query["metadata"][field] = cgi[field][0]
            elif cgi[field][0] != '':
                query["metadata"][field] = cgi[field][0]
        if field not in cgi or not cgi[field][0]: ## in case of an empty query
            num_empty += 1
            
    if re.search('([A-Z]+|\*)', query['q']):
        query['q'] = crapser(query['q'])
        print >> sys.stderr, query['q']
                
    return query, db

if  __name__ == '__main__':
    form = cgi.FieldStorage()
    query = form.getvalue('q')
    path = os.environ['SCRIPT_FILENAME']
    path = path.replace('scripts/get_hit_num.py', '')
    path += 'data/'
    query, db = parse_cgi(query, path)
    hits = db.query(query["q"],query["method"],query["arg"],**query["metadata"])
    print "Content-Type: text/html\n"
    print len(hits)
    

