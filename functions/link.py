#!/usr/bin/env python
import urllib
from wsgiref.util import shift_path_info
import urlparse
import re
import sys
import os
from philologic.DB import DB
from scripts.crapser import *


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
    if start > results_len:
        start = results_len - 1
    if start <= 0:
        start = 1
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