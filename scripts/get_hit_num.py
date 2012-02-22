#!/usr/bin/env python

import os
import sys
import cgi
from philologic.PhiloDB import PhiloDB

if  __name__ == '__main__':
    sys.path.append('../')
    from philo_helpers import parse_cgi
    form = cgi.FieldStorage()
    query = form.getvalue('q')
    db, query = parse_cgi(os.environ, q=query)
    print >> sys.stderr, query
    hits = db.query(query["q"],query["method"],query["arg"],**query["metadata"])
    print "Content-Type: text/html\n"
    print len(hits)
    

