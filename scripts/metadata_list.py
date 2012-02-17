#!/usr/bin/env python

import os
import cgi
import sys
import json
from philologic.PhiloDB import PhiloDB
    
def autocomplete_metadata(metadata, field, db):
    conn = db.toms.dbh
    c = conn.cursor()
    
    ## Workaround for when jquery sends a list of words: this happens when using the back button
    if isinstance(metadata, list):
        metadata = metadata[-1]
        field = field[-1]    

    start = metadata + '_%'
    middle = '_% ' + metadata + '_%'
    query = "select %s from toms where %s like '%s' or %s like '%s' group by %s order by count(%s) desc" % (field, field, start, field, middle, field, field)   
    c .execute(query)
    result_list = []
    for result in c.fetchall():
        result_list.append(result[0])
        if len(result_list) == 10:
            break
    return json.dumps(result_list)

if __name__ == "__main__":
    path = os.environ['SCRIPT_FILENAME']
    path = path.replace('scripts/metadata_list.py', '')
    path += 'data/'
    db = PhiloDB(path)
    form = cgi.FieldStorage()
    metadata = form.getvalue('term')
    field = form.getvalue('field')
    content = autocomplete_metadata(metadata, field, db)
    print "Content-Type: text/html\n"
    print content
    