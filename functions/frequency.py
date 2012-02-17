from philo_helpers import make_query_link

def frequency(results, q):
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
    return field, sorted(counts.iteritems(), key=lambda x: x[1], reverse=True)