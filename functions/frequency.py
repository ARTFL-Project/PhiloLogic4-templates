from __future__ import division
from mako.template import Template
from mako.lookup import TemplateLookup
from philo_helpers import make_query_link

def frequency(h, HitWrapper, IRHitWrapper, path, db, dbname, q, environ):
    mytemplates = TemplateLookup(path)
    template = Template(filename="templates/frequency.mako", lookup=mytemplates)
    hits = db.query(q["q"],q["method"],q["arg"],**q["metadata"])
    results = HitWrapper.results_wrapper(hits,db)
    try:
        return template.render(results=results,db=db,dbname=dbname,q=q,generate_frequency=generate_frequency,h=h).encode("UTF-8", "ignore")
    except:
        return exceptions.html_error_template().render()

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