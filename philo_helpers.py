#!/usr/bin/env python
import urllib
from wsgiref.util import shift_path_info
import urlparse
import re
import sys
import os
from philologic.DB import DB
from scripts.crapser import *

### CGI PARAMETER PARSING ###

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
    
### CITATIONS ###
    
def make_div_cite(i):
    """ Returns a representation of a PhiloLogic object and all it's ancestors suitable for a precise concordance citation. """
    doc_href = make_object_link(i.philo_id[:1],i.bytes)
    section_href = make_object_link(i.philo_id[:2], i.bytes)
    sub_section_href = make_object_link(i.philo_id[:3], i.bytes)
    para_href = make_object_link(i.philo_id[:5], i.bytes)
    section_names = [i.div1.head,i.div2.head,i.div3.head]
    section_name = section_names[0]
    try:
        sub_section_name = section_names[1]
    except IndexError:
        sub_section_name = section_name
    speaker_name = i.who
    cite = u"<span class='philologic_cite'>%s <a href='%s' title='title'>%s</a>" % (i.author,doc_href,i.title)
    if section_name:
        cite += u" - <a href='%s'>%s</a>" % (section_href,section_name)
    if sub_section_name:
        cite += u" - <a href='%s'>%s</a>" % (sub_section_href,sub_section_name)
    cite += "</span>"
    return cite
    
def make_doc_cite(i):
    """ Returns a representation of a PhiloLogic object suitable for a bibliographic report. """
    doc_href = make_object_link(i.philo_id[:1], i.bytes)
    record = u"%s, <i><a href='%s'>%s</a></i> [%s]" % (i.author, doc_href,i.title, i.date)
    return record

### LINKING ###

def hit_to_link(db,hit):
    ## We should remove this function, it has been superseded.
    i = 0
    partial = []
    best = []
    for n,k in enumerate(hit):
        partial.append(k)
        if partial in db.toms and db.toms[partial]["philo_name"] != "__philo_virtual":
            best = partial[:]
        else:
            break
    return "./" + "/".join(str(b) for b in best)

def make_query_link(query,method=None,methodarg=None,report=None,start=None,end=None,results_per_page=None,**metadata): 
    """ Takes a dictionary of query parameters as produced by parse_cgi, and returns a relative URL representation of such. """
    try:
        q_params = [("q",query.encode('utf-8', 'ignore'))] ## urlencode does not like unicode...
    except UnicodeDecodeError:
        q_params = [("q",query)]
    if method:
        q_params.append(("method",method))
    if methodarg:
        q_params.append(("arg",methodarg))
    try:
        metadata = dict([(k, v.encode('utf-8', 'ignore')) for k, v in metadata.items()])
    except UnicodeDecodeError:
        pass
    q_params.extend(metadata.items()[:])
    if report:
        q_params.append(("report",report))
    if start:
        q_params.append(("start" , start))
    if end:
        q_params.append(("end", end))
    if results_per_page:
        q_params.append(("results_per_page", results_per_page))
    return "./?" + urllib.urlencode(q_params)

def make_object_link(philo_id, hit_bytes):
    """ Takes a valid PhiloLogic object, and returns a relative URL representation of such. """
    href = "./" + "/".join(str(x) for x in philo_id) + byte_query(hit_bytes)
    return href

def make_absolute_object_link(db,id,bytes = []):
    """ Takes a valid PhiloLogic object, and returns an absolute URL representation of such. """
    href = db.locals["db_url"] +"/dispatcher.py/" + "/".join(str(x) for x in id)
    if bytes:
        href += byte_query(bytes)
    return href
    
def make_absolute_query_link(db,**params):
    """ Takes a dictionary of query parameters as produced by parse_cgi, and returns an absolute URL representation of such. """
    pass
    
def byte_query(hit_bytes):
    """This is used for navigating concordance results and highlighting hits"""
    return '?' + '&'.join(['byte=%d' % int(byte) for byte in hit_bytes])

def page_interval(num, results_len, start, end):
    if start <= 0:
        start = 1
    if start > results_len:
        start = results_len - 1
    if end <= 0:
        end = start + (num - 1)
    if end > results_len:
        end = results_len
    n = start - 1
    return start, end, n
    
def page_links(start, end, results_per_page, q, results_len):
    prev_start = start - results_per_page
    prev_end = end - results_per_page
    next_start = start + results_per_page
    next_end = end + results_per_page
    if next_start > results_len and prev_start < 0:
        prev_page = ''
        next_page = ''
    elif next_start > results_len:
        next_page = ''
        prev_end = start - 1
        prev_page = make_query_link(q["q"],q["method"],q["arg"],q['report'],prev_start,prev_end,results_per_page,**q["metadata"])
    else:
        if prev_start > 0:
            prev_page = make_query_link(q["q"],q["method"],q["arg"],q['report'],prev_start,prev_end,results_per_page,**q["metadata"])
        else:
            prev_page = ''
        next_page = make_query_link(q["q"],q["method"],q["arg"],q['report'],next_start,next_end,results_per_page,**q["metadata"])
    
    return prev_page, next_page

### TEI FORMATTING ###
