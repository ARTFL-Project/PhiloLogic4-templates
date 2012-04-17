#!/usr/bin/env python

from MakoWrapper import render_template

def bibliography(HitWrapper, q, db, dbname):
    if q["no_q"]:
            hits = db.toms.get_documents()
    else:
        hits = db.toms.query(**q["metadata"])
    results = HitWrapper.metadata_results_wrapper(hits, db)
    return render_template(results=results,db=db,dbname=dbname,q=q, template_name='bibliography.mako')