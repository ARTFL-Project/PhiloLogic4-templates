#!/usr/bin/env python
import urllib
from wsgiref.util import shift_path_info
import urlparse
import re
import sys
import os
from philologic.DB import DB
from scripts.crapser import *

sys.path.append('../scripts/')

def parse_cgi(environ):
    """ Parses CGI parameters from Apache, returns a tuple with a philologic database, remaining path components, and a query dict. """
    myname = environ["SCRIPT_FILENAME"]
    myname = myname.replace('scripts/get_hit_num.py', '') ## when get_hit_num calls this function
    dbfile = os.path.dirname(myname) + "/data"
    db = DB(dbfile,encoding='utf-8')
    print >> sys.stderr, environ["QUERY_STRING"]
    cgi = urlparse.parse_qs(environ["QUERY_STRING"],keep_blank_values=True)
   
    query = {}
    query["q"] = cgi.get("q",[None])[0]
    query["method"] = cgi.get("method",[None])[0] 
    query["arg"] = cgi.get("arg",[0])[0]
    query["report"] = cgi.get("report",[None])[0]
    query["format"] = cgi.get("format",[None])[0]
    query["results_per_page"] = int(cgi.get("results_per_page",[50])[0])
    
    ## Hack so that even if there are multiple byte offsets
    ## we still have it stored as a string in query
    query["byte"] = '+'.join(cgi.get("byte",['']))
    
    ## This defines within how many words for collocation tables
    query["word_num"] = int(cgi.get("word_num",[0])[0])
    
    # This defines the collocate for collocation to concordance searches
    query["collocate"] = cgi.get("collocate",[None])[0]
    
    ## This is for frequency searches: raw count or per n number of words
    query["rate"] = cgi.get("rate", [None])[0]
    
    ## This is for ranked relevancy
    query['obj_type'] = 'doc'
    
#    query["dbname"] = dbname
    query["dbpath"] = dbfile
    query["start"] = int(cgi.get('start',[0])[0]) # special range handling done in each service now.
    query["end"] = int(cgi.get('end',[0])[0]) 
    query["width"] = int(cgi.get("width",[0])[0]) or 300
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
    
    if num_empty == len(metadata_fields):
        query["no_q"] = True
    else:
        query["no_q"] = False
    
    if query['q']:  
        if re.search('([A-Z]+|\*)', query['q']):
            query['q'] = crapser(query['q'])
    
    path_components = [c for c in environ["PATH_INFO"].split("/") if c]
    try:
        if path_components[0] == 'form':
            query['report'] = 'form'
    except IndexError:
        path_components = False
    
    return (db, path_components, query)    