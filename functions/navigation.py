#!/usr/bin/env python

import sqlite3
import re
import sys
from MakoWrapper import render_template
from HitWrapper import *
from format import *

philo_types = set(['div1', 'div2', 'div3'])

def navigation(h, path, path_components, db, dbname, q, environ):
    obj = hit_wrapper(path_components,None,db)
    doc = db[path_components[0]]
    return render_template(obj=obj,dbname=dbname,doc=doc,path_components=path_components,
                           navigate_doc=navigate_doc,navigate_object=navigate_object,db=db,q=q, form=False, template_name='object.mako')

def navigate_doc(philo_id, db):
    conn = db.toms.dbh ## make this more accessible 
    c = conn.cursor()
    query =  philo_id + " _%"
    c.execute("select philo_id, philo_name, philo_type, byte_start from toms where philo_id like ?", (query,))
    text_hierarchy = []
    for id, philo_name, philo_type, byte in c.fetchall():
        if philo_type not in philo_types or philo_name == '__philo_virtual':
            continue
        id = re.sub(' 0$', '', id)
        hit_object = object_wrapper(id.split(), byte, db, obj_type=philo_type)
        obj_name = getattr(hit_object, philo_type)
        text_hierarchy.append(hit_object)
    return text_hierarchy

def navigate_object(obj, query_args=False):
    path = "./data/TEXT/" + obj.filename
    file = open(path)
    byte_start = obj.byte_start
    file.seek(byte_start)
    width = obj.byte_end - byte_start
    raw_text = file.read(width)
    if query_args:
        bytes = sorted([int(byte) - byte_start for byte in query_args.split('+')])
        text_start, text_middle, text_end = chunkifier(raw_text, bytes, highlight=True)
        raw_text = text_start + text_middle + text_end
        ## temp hack until we work out how to format without loosing highlight
        ## tags
        raw_text = re.sub('<(/?span[^>]*)>', '[\\1]', raw_text)
        text_obj = formatter(raw_text).decode("utf-8","ignore")
        return text_obj.replace('[', '<').replace(']', '>')
    else:
        return formatter(raw_text).decode("utf-8","ignore")