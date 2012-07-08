#!/usr/bin/env python

import os
import re
import sys
sys.path.append('..')
import functions as f
import reports as r
import cgi
import json
from philologic.DB import DB


def generate_link(field, metadata_field, query):
    link_metadata = {}
    link_metadata[metadata_field] = field[:]
    if len(field) > 40: ## limit length for display purposes
        field = field[:40].encode('utf-8', 'ignore') + '...'
    url = f.link.make_query_link(query, 'proxy', '', **link_metadata)
    link = '<a href="%s">' % url + field + '</a>'
    return link

def get_frequency_for_one_term(query, metadata_field, db):
    c = db.dbh.cursor()
    query = query.decode('utf-8', 'ignore')
    sql_query = 'select philo_id, doc_token_count from doc_word_counts where philo_name=? order by doc_token_count desc'
    c.execute(sql_query, (query,))
    results = {}
    for i in c.fetchall():
        sql_query = 'select %s from toms where philo_id=?' % metadata_field
        c.execute(sql_query, (i[0],))
        field = c.fetchone()[0].decode('utf-8', 'ignore')
        link = generate_link(field, metadata_field, query) 
        if link not in results:
            results[link] = 0 
        results[link] += int(i[1])
    results = sorted(results.iteritems(), key=lambda x: x[1], reverse=True)[:50]
    return json.dumps(results)
    
def get_frequency_for_multiple_terms(query, metadata_field, db):
    hits = db.query(term,'','',**{})
    q = {"field": metadata_field, "rate": ""}
    metadata_field, freq_results = r.generate_frequency(hits, q, db)
    results = {}
    for field, count in freq_results:
        link = generate_link(field, metadata_field, query)
        if link not in results:
            results[link] = 0 
        results[link] += count
    results = sorted(results.iteritems(), key=lambda x: x[1], reverse=True)[:50]
    return json.dumps(results)
    
if __name__ == "__main__":
    path = os.environ['SCRIPT_FILENAME']
    path = re.sub('(philo4/[^/]+/).*', '\\1', path)
    db = DB(path + '/data/')
    form = cgi.FieldStorage()
    term = form.getvalue('term')
    field = form.getvalue('field')
    if re.search('[ |]+', term):
        results = get_frequency_for_multiple_terms(term, field, db)
    else:
        results = get_frequency_for_one_term(term, field, db)
    print "Content-Type: text/html\n"
    print results
    