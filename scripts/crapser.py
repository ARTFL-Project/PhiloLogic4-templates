#!/usr/bin/env python

import os
import cgi
import subprocess
import sys
import re

    
def crapser(term):
    """ Expand queries"""
    ## Find path to all_frequencies
    path = os.environ['SCRIPT_FILENAME']
    path = path.replace('dispatcher.py', '')
    path += 'data/WORK/all_frequencies'
    
    ## Add wildcard and search for pattern
    term = term.replace('*', '\w*')
    command = ['egrep', '-oie', "%s" % term, '%s' % path]
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    match, stderr = process.communicate()
    matching_list = set(match.split('\n'))
    print >> sys.stderr,  matching_list
    
def sql_crapser(term, field, db):
    """Expand metadata queries"""
    conn = db.toms.dbh
    c = conn.cursor()
    
    ## Add wildcard and search for pattern
    term = term.replace('*', '_%')
    query = 'select %s from toms where %s like "%s"' % (field, field, term)
    print >> sys.stderr, query
    c.execute(query)
    matching_list = [i[0] for i in c.fetchall()]
    print >> sys.stderr,  matching_list