#!/usr/bin/env python

import os
import re
import sys
sys.path.append('..')
import functions as f
import cgi
import json
from philologic.DB import DB

def get_frequency(query, metadata_field):
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
        sql_query = 'select %s from toms where philo_id=?' % metadata_field
        c.execute(sql_query, (i[0],))
        field = c.fetchone()[0]
        link_metadata = {}
        link_metadata[metadata_field] = field[:]
        if len(field.decode('utf_8', 'ignore')) > 40: ## limit length for display purposes
            field = field.decode('utf_8', 'ignore')[:40].encode('utf-8', 'ignore') + '...'
        url = f.link.make_query_link(query, 'proxy', '', **link_metadata)
        link = '<a href="%s">' % url + field + '</a>' 
        if link not in results:
            results[link] = 0 
        results[link] += int(i[1])
    results = sorted(results.iteritems(), key=lambda x: x[1], reverse=True)[:50]
    return json.dumps(results)
    
if __name__ == "__main__":
    form = cgi.FieldStorage()
    term = form.getvalue('term')
    field = form.getvalue('field')
    results = get_frequency(term, field)
    print "Content-Type: text/html\n"
    print results
    