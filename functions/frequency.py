from __future__ import division
from philo_helpers import make_query_link

def frequency(results, q, db):
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