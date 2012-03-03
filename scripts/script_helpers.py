#!/usr/bin/env python

import re
import os
import subprocess

def frequencies_file(environ, field_type):
    path = environ['SCRIPT_FILENAME']
    path = re.sub('(philo4/[^/]+/).*', '\\1', path)
    path += 'data/frequencies/%s_frequencies' % field_type
    return path

def word_pattern_search(term, path):
    term = term.replace('*', '.*')
    command = ['egrep', '-oie', "%s\W" % term, '%s' % path]
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    match, stderr = process.communicate()
    return [m.strip() for m in match.split('\n')]
    
def metadata_pattern_search(term, path):
    term = '(.* |^)%s.*' % term
    command = ['egrep', '-oie', "%s\W" % term, '%s' % path]
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    match, stderr = process.communicate()
    return [m.strip() for m in match.split('\n')]