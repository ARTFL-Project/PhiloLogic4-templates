#!/usr/bin/env python

import os
import urlparse
import reports
from wsgiref.handlers import CGIHandler
from cgi import FieldStorage

def philo_dispatcher(environ,start_response):
    report = FieldStorage().getvalue('report')
    path_components = [c for c in environ["PATH_INFO"].split("/") if c]
    if path_components:
        if path_components[0] == "form":
            yield reports.form(start_response, environ)
        else:
            yield getattr(reports, report or "navigation")(start_response, environ)
    else:
        yield getattr(reports, report or "concordance")(start_response, environ)
        
if __name__ == "__main__":
    CGIHandler().run(philo_dispatcher)
