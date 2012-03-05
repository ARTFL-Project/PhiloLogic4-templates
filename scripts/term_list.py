#!/usr/bin/env python

import os
import cgi
import sys
import json
from script_helpers import *

    
def autocomplete_term(word_start):
    path = frequencies_file(os.environ, 'word')
    
    ## Workaround for when jquery send a list of words: happens when using the back button
    if isinstance(word_start, list):
        word_start = word_start[-1]
        
    word_start +='*'
    words = word_pattern_search(word_start, path)[:10]
    return json.dumps(words)

if __name__ == "__main__":
    form = cgi.FieldStorage()
    term = form.getvalue('term')
    content = autocomplete_term(term)
    print "Content-Type: text/html\n"
    print content
    