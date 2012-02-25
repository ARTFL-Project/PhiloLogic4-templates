#!/usr/bin/env python

import re
import os
import subprocess

def word_frequencies_file(environ):
    path = environ['SCRIPT_FILENAME']
    path = re.sub('(philo4/[^/]+/).*', '\\1', path)
    path += 'data/WORK/all_frequencies'
    return path

def word_pattern_search(term, path):
    term = term.replace('*', '.*')
    command = ['egrep', '-oie', " %s" % term, '%s' % path]
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    match, stderr = process.communicate()
    return [m.strip() for m in match.split('\n')]