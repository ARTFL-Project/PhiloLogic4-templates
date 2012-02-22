#!/usr/bin/env python
import sys
import os
import urlparse

from wsgiref.handlers import CGIHandler
from wsgiref.util import shift_path_info
from philologic.PhiloDB import PhiloDB
from philo_helpers import *
from HitWrapper import *
from mako.template import Template
from mako.lookup import TemplateLookup
import functions

def philo_dispatcher(environ,start_response):
    status = '200 OK'
    headers = [('Content-type', 'text/html; charset=UTF-8'),("Access-Control-Allow-Origin","*")]
    start_response(status,headers)
    environ["parsed_params"] = urlparse.parse_qs(environ["QUERY_STRING"],keep_blank_values=True)
    cgi = environ["parsed_params"]
    myname = environ["SCRIPT_FILENAME"]
    dbname = os.path.basename(myname.replace("/dispatcher.py",""))
    reports = os.listdir("./templates")
    scripts = os.listdir("./scripts")
    db,q = parse_cgi(environ)
    mytemplates = TemplateLookup('./')
    path = os.getcwd()
    try:
        path_components = [c for c in environ["PATH_INFO"].split("/") if c]
    except KeyError:
        path_components = False
    if path_components:
        if path_components[0] == "form":
            yield (Template(filename="./templates/form.mako", lookup=mytemplates).render(db=db,dbname=dbname,
                            reports=reports, form=True).encode("UTF-8"))
            return
        obj = hit_wrapper(path_components,None,db)
        doc = db[path_components[0]]
        yield(Template(filename="./templates/object.mako", lookup=mytemplates).render(obj=obj,dbname=dbname,doc=doc,
                        path_components=path_components, navigate_doc=functions.navigate_doc,navigate_object=functions.navigate_object,db=db,q=q, form=False).encode("UTF-8"))
        return
    else:        
        function = getattr(functions, q["report"] or "concordance")
        if q["q"] == None or q["q"] == '':
            if q["report"] == 'concordance':
                template_name = "./templates/" + "bibliography" + '.mako'
            else:
                template_name = "./templates/" + q["report"] + '.mako'
            template = Template(filename=template_name, lookup=mytemplates)
            if q["no_q"]:
                hits = db.toms.get_documents()
            else:
                hits = db.toms.query(**q["metadata"])
            results = metadata_results_wrapper(hits, db) 
            yield template.render(results=results,db=db,dbname=dbname,q=q,report_function=function,path=path,make_query_link=make_query_link, form=False).encode("UTF-8")
        else:
            template_name = "./templates/" + (q["report"] or "concordance") + '.mako'
            template = Template(filename=template_name, lookup=mytemplates)
            hits = db.query(q["q"],q["method"],q["arg"],**q["metadata"])
            results = results_wrapper(hits,db)
            yield template.render(results=results,db=db,dbname=dbname,q=q,report_function=function,
                                  format=functions.format, path=path, hitnum=len(hits), make_query_link=make_query_link,
                                  make_object_link=make_object_link,page_interval=page_interval,page_links=page_links,
                                  byte_query=byte_query, results_per_page=q['results_per_page'], form=False,
                                  q_string = environ['QUERY_STRING']).encode("UTF-8")
        
        
        
        
if __name__ == "__main__":
    CGIHandler().run(philo_dispatcher)
