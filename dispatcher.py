#!/usr/bin/env python

import os
import urlparse
from wsgiref.handlers import CGIHandler
import reports
from functions import parse_cgi


def philo_dispatcher(environ,start_response):
    status = '200 OK'
    headers = [('Content-type', 'text/html; charset=UTF-8'),("Access-Control-Allow-Origin","*")]
    start_response(status,headers)
    environ["parsed_params"] = urlparse.parse_qs(environ["QUERY_STRING"],keep_blank_values=True)
    myname = environ["SCRIPT_FILENAME"]
    dbname = os.path.basename(myname.replace("/dispatcher.py",""))
    db, path_components, q = parse_cgi(environ)
    path_components = [c for c in environ["PATH_INFO"].split("/") if c]
    path = os.getcwd()
    if path_components:
        if path_components[0] == "form":
            yield reports.form(path,path_components,db,dbname,q,environ)
        else:
            yield getattr(reports, q["report"] or "navigation")(path, path_components, db, dbname, q, environ)
    else:
        yield getattr(reports, q["report"] or "concordance")(path, path_components, db, dbname, q, environ)
        
if __name__ == "__main__":
    CGIHandler().run(philo_dispatcher)
