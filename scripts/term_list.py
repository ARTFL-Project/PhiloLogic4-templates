#!/usr/bin/env python

import os
import cgi
import sys
import json

def read_file():
    path = os.environ['SCRIPT_FILENAME']
    path = path.replace('scripts/term_list.py', '')
    path += 'data/WORK/all_frequencies'
    return open(path)
    
def autocomplete_term(word_start):
    words = []
    filehandle = read_file()
    
    ## Workaround for when jquery send a list of words: happens when using the back button
    if isinstance(word_start, list):
        word_start = word_start[-1]
    
    for line in filehandle:
        freq, word = line.split()
        if word.startswith(word_start):
            words.append(word)
        if len(words) == 10:
            break
    filehandle.close()
    return json.dumps(words)

if __name__ == "__main__":
    form = cgi.FieldStorage()
    term = form.getvalue('term')
    content = autocomplete_term(term)
    print "Content-Type: text/html\n"
    print content
    