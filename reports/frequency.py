#!/usr/bin env python
from __future__ import division
import sys
sys.path.append('..')
import functions as f
from functions.wsgi_handler import wsgi_response
from render_template import render_template
import json

def frequency(start_response, environ):
    db, dbname, path_components, q = wsgi_response(start_response, environ)
    hits = db.query(q["q"],q["method"],q["arg"],**q["metadata"])
    if q["format"] == "json":
        field, counts = generate_frequency(hits,q,db)
        l = len(counts)
        wrapper = {"length":l,"result":[],"field":field}
        for k,v in counts:
            q["metadata"][field] = '"%s"' % k or "NULL"
            url = make_query_link(q["q"],q["method"],q["arg"],**q["metadata"])
            table_row = {"label":k,"count":v,"url":url}
            wrapper["result"].append(table_row)
        return json.dumps(wrapper,indent=1)
        
    else:
        return render_template(results=hits,db=db,dbname=dbname,q=q,generate_frequency=generate_frequency,f=f, template_name='frequency.mako')

def generate_frequency(results, q, db):
    field = q["field"]
    if field == None:
        field = 'title'
    counts = {}
    for n in results:
        label = n[field]
        if label == '':
            label = 'NULL'
        if label not in counts:
            counts[label] = 0
        counts[label] += 1
    if q['rate'] == 'relative':
        conn = db.dbh ## make this more accessible 
        c = conn.cursor()
        for label, count in counts.iteritems():
            counts[label] = relative_frequency(field, label, count, c)
    return field, sorted(counts.iteritems(), key=lambda x: x[1], reverse=True)
    
def relative_frequency(field, label, count, c):
    query = '''select sum(word_count) from toms where %s="%s"''' % (field, label)
    c.execute(query)
    return count / c.fetchone()[0] * 10000
