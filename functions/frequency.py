#!/usr/bin env python

from __future__ import division
from MakoWrapper import render_template
from philo_helpers import make_query_link

def frequency(h, HitWrapper, IRHitWrapper, path, db, dbname, q, environ):
    hits = db.query(q["q"],q["method"],q["arg"],**q["metadata"])
    results = HitWrapper.results_wrapper(hits,db)
    return render_template(results=results,db=db,dbname=dbname,q=q,generate_frequency=generate_frequency,h=h, template_name='frequency.mako')

def generate_frequency(results, q, db):
    field = q["field"]
    if field == None:
        field = 'title'
    counts = {}
    for n in results:
        label = n[field]
        if label == '':
            label = 'Unknown'
        if label in counts:
            counts[label] += 1
        else:
            counts[label] = 1
    if q['rate'] == 'relative':
        conn = db.toms.dbh ## make this more accessible 
        c = conn.cursor()
        for label, count in counts.iteritems():
            counts[label] = relative_frequency(field, label, count, c)
    return field, sorted(counts.iteritems(), key=lambda x: x[1], reverse=True)
    
def relative_frequency(field, label, count, c):
    query = '''select sum(word_count) from toms where %s="%s"''' % (field, label)
    c.execute(query)
    return count / c.fetchone()[0] * 10000