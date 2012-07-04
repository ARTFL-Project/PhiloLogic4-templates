#!/usr/bin/env python

import os
import re
import sqlite3
import sys
import cgi
import json
from philologic.DB import DB

def get_frequency(query):
    path = os.environ['SCRIPT_FILENAME']
    path = re.sub('(philo4/[^/]+/).*', '\\1', path)
    db = DB(path + '/data/').dbh
    c = db.cursor()
    philo_names = []
    for q in query.split():
        philo_names.append('philo_name="%s"' % q)
    philo_names = ' '.join(philo_names)
    sql_query = 'select philo_id, doc_token_count from doc_word_counts where %s order by doc_token_count desc' % philo_names
    c.execute(sql_query)
    results = {}
    for i in c.fetchall():
        sql_query = 'select author from toms where philo_id=?'
        c.execute(sql_query, (i[0],))
        field = c.fetchone()[0]
        if len(field.decode('utf_8', 'ignore')) > 40: ## limit length for display purposes
            field = field.decode('utf_8', 'ignore')[:40].encode('utf-8', 'ignore') + '...'
        if field not in results:
            results[field] = 0 
        results[field] += int(i[1])
    results = sorted(results.iteritems(), key=lambda x: x[1], reverse=True)[:50]
    print >> sys.stderr, results
    return json.dumps(results)
    
if __name__ == "__main__":
    form = cgi.FieldStorage()
    term = form.getvalue('term')
    results = get_frequency(term)
    print "Content-Type: text/html\n"
    print results
    