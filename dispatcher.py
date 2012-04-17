#!/usr/bin/env python

import os
import urlparse
from wsgiref.handlers import CGIHandler
import functions
import philo_helpers as h
import HitWrapper
import IRHitWrapper


def philo_dispatcher(environ,start_response):
    status = '200 OK'
    headers = [('Content-type', 'text/html; charset=UTF-8'),("Access-Control-Allow-Origin","*")]
    start_response(status,headers)
    environ["parsed_params"] = urlparse.parse_qs(environ["QUERY_STRING"],keep_blank_values=True)
    myname = environ["SCRIPT_FILENAME"]
    dbname = os.path.basename(myname.replace("/dispatcher.py",""))
    db, path_components, q = h.parse_cgi(environ)
    path = os.getcwd()
    if path_components:
        yield getattr(functions, q["report"] or "navigation")(h, path, path_components, db, dbname, q, environ)
    else:
        yield getattr(functions, q["report"] or "form")(h, HitWrapper, IRHitWrapper, path, db, dbname, q, environ)
        
if __name__ == "__main__":
    CGIHandler().run(philo_dispatcher)
