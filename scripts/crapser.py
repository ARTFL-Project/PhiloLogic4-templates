#!/usr/bin/env python

import os
import cgi
import subprocess
import sys

def read_file():
    path = os.environ['SCRIPT_FILENAME']
    path = path.replace('dispatcher.py', '')
    path += 'data/WORK/all_frequencies'
    return path

def expand_term(term):
    file = read_file()
    command = ['egrep', '-oie', "%s\w*" % term, '%s' % file]
    print >> sys.stderr, command
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    match, stderr = process.communicate()
    matching_list = set(match.split('\n'))
    return matching_list    
    
def crapser(term):
    form = cgi.FieldStorage()
    word = form.getvalue('term')
    words = expand_term(term)
    print >> sys.stderr,  words