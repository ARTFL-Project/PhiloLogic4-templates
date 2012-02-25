#!/usr/bin/env python

import os
import cgi
import subprocess
import sys
import re
from script_helpers import *


accents = {'A': "(a|\xc3\xa0|\xc3\xa1|\xc3\xa2|\xc3\xa3|\xc3\xa4|\xc3\x82)",
           'C': "(c|\xc3\xa7|\xc3\x87)",
           'E': "(e|\xc3\xa8|\xc3\xa9|\xc3\xaa|\xc3\xab|\xc3\x89|\xc3\x88|\xc3\x8A)",
           'I': "(i|\xc3\xac|\xc3\xad|\xc3\xae|\xc3\xaf)",
           'N': "(n|\xc3\xb1)",
           'O': "(o|\xc3\xb2|\xc3\xb3|\xc3\xb4|\xc3\xb4|\xc3\xb6|\xc3\x94)",
           'U': "(u|\xc3\xb9|\xc3\xba|\xc3\xbb|\xc3\xbc)",  
           'Y': "(y|\xc3\xbf|xc3\xbd)"}

def expand_query(term, path):
    ## Look for uppercase letters and replace with regex pattern
    for uppercase in accents:
        if term.find(uppercase) != -1:
            term = term.replace(uppercase, accents[uppercase])
    
    ## Add wildcard and search for pattern
    term = term.replace('*', '.*')
    matching_list = word_pattern_search(term, path)
    matching_list = [i for i in matching_list if i]
    matching_list = '|'.join(matching_list)
    return matching_list

def crapser(term):
    """ Expand queries"""
    ## Find path to all_frequencies
    path = word_frequencies_file(os.environ)
    
    ## Iterate through query
    matching_list = ''
    for t in term.split():
        matching_list += expand_query(t, path) + ' '
 
    return matching_list.rstrip()
    
def sql_crapser(term, field, db):
    """Expand metadata queries"""
    ## Open SQL cursor
    conn = db.toms.dbh
    c = conn.cursor()  
    
    ## Add wildcard and search for pattern
    term = term.replace('*', '_%')
    query = 'select %s from toms where %s like "%s"' % (field, field, term)
    c.execute(query)
    matching_list = [i[0] for i in c.fetchall()]
    print >> sys.stderr,  matching_list