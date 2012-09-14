#!/usr/bin/env python

from __future__ import division
import sys
sys.path.append('..')
import functions as f
import sqlite3
import os
from functions.wsgi_handler import wsgi_response
from math import log
from random import sample
from philologic.DB import DB
from functions.format import adjust_bytes, chunkifier, clean_text, align_text
from bibliography import bibliography
import re
from render_template import render_template


def relevance(start_response, environ):
    db, dbname, path_components, q = wsgi_response(start_response, environ)
    path = os.getcwd().replace('functions/', '')
    
    if q['q'] == '':
        return bibliography(f,path, db, dbname,q,environ)
    else:
        results = retrieve_hits(q, db)
    return render_template(results=results,db=db,dbname=dbname,q=q,fetch_relevance=fetch_relevance,f=f,format=format,
                                path=path, results_per_page=q['results_per_page'], template_name='relevance.mako')

def filter_hits(q, obj_types, c):
    ## Filter out if necessary
    philo_ids = []
    total_docs = int
    for field in q['metadata']:
        if field != 'n' and q['metadata'][field] != '':
            for obj_type in obj_types:
                query = 'select philo_id from toms where %s=? and philo_type=?' % field
                c.execute(query, (q['metadata'][field], obj_type))
                results = [i[0] for i in c.fetchall()]
                philo_ids.extend(results)
    if philo_ids:
        philo_ids = set(philo_ids)
        total_docs = len(philo_ids)
    else:
        query = 'select count(*) from toms where '
        query += ' or '.join(['philo_type="%s"' % i for i in obj_types])
        query += ' and philo_name != "__philo_virtual"'
        print >> sys.stderr, query
        c.execute(query)
        total_docs = int(c.fetchone()[0])
    return philo_ids, total_docs

def compute_idf(query_words, table, c, total_docs):
    ## Compute IDF
    idfs = {}
    for word in query_words.split():
        c.execute('select count(*) from %s where philo_name=?' % table, (word,))
        docs_with_word = int(c.fetchone()[0]) or 1  ## avoid division by 0
        doc_freq = total_docs / docs_with_word
        if doc_freq == 1:
            doc_freq = (total_docs + 1) / docs_with_word ## The logarithm won't be equal to 0
        idf = log(doc_freq)
        idfs[word] = idf
    return idfs

def retrieve_hits(q, db):
    object_types = ['doc', 'div1', 'div2', 'div3', 'para', 'sent', 'word']
    obj_types = db.locals['ranked_relevance_objects']
    table = db.locals['ranked_relevance_table_name']
    
    ## Get the depths for philo_id slices
    #depths = []
    #for obj_type in obj_types:
    #    depths.append(object_types.index(obj_type) + 1)
    
    
    ## Open cursors for sqlite tables
    conn = db.dbh
    c = conn.cursor()
    philo_ids, total_docs = filter_hits(q, obj_types, c)
    
    query_words = q['q'].replace('|', ' ') ## Handle ORs from crapser
    q['q'] = q['q'].replace(' ', '|') ## Add ORs for search links
    
    idfs = compute_idf(query_words, table, c, total_docs)
    
    #print >> sys.stderr, "###DEBUG###", query_words, idfs[query_words]
    
    ## Construct query
    c.execute('select * from %s limit 1' % table)
    fields = ['%s.' % table + i[0] for i in c.description]
    c.execute('select * from toms limit 1')
    extra_fields = ['toms.' + i[0] for i in c.description if '%s.%s' % (table, i[0]) not in fields]
    fields.extend(extra_fields)
    if len(query_words.split()) > 1:
        query = 'select %s from %s inner join toms on toms.philo_id=%s.philo_id and toms.philo_name!="__philo_virtual" where ' % (','.join(fields), table, table)
        words =  query_words.split()
        query += ' or '.join(['%s.philo_name=?' % table for i in words])
        c.execute(query, words)
    else:
        query = 'select %s from %s inner join toms on toms.philo_id=%s.philo_id and toms.philo_name!="__philo_virtual" where %s.philo_name=?' % (','.join(fields),table, table, table)
        #print >> sys.stderr, "#QUERY#", query
        c.execute(query, (query_words,))
    
    new_results = {}
    for i in c.fetchall():
        philo_id = i['philo_id']
        philo_name = i['philo_name']
        token_counts = i['token_count']
        bytes = i['bytes']
        word_count = i['word_count']
        boost = metadata_boost(philo_name, q['metadata'], i)
        if not philo_ids or philo_id in philo_ids:
            total_word_count = int(word_count)
            term_frequency = token_counts/total_word_count
            tf_idf = term_frequency * idfs[philo_name]
            if philo_id not in new_results:
                new_results[philo_id] = {}
                new_results[philo_id]['obj_type'] = object_types[philo_id.split().index('0') - 1]
                new_results[philo_id]['bytes'] = []
                new_results[philo_id]['tf_idf'] = 0
            new_results[philo_id]['tf_idf'] += tf_idf * boost
            new_results[philo_id]['bytes'].extend(bytes.split())
    hits = sorted(new_results.iteritems(), key=lambda x: x[1]['tf_idf'], reverse=True)
    #print >> sys.stderr, hits
    return f.IRHitWrapper.ir_results_wrapper(hits, db)
    
    
def metadata_boost(word, metadata, i):
    boost = 0
    for field in metadata:
        try:
            field = i[field].decode('utf-8', 'ignore').lower().encode('utf-8', 'ignore')
            if re.search(word, field):
                boost += 4
        except (IndexError, TypeError, AttributeError):
            pass
    return boost or 1
 
def fetch_relevance(hit, path, q, kwic=True, samples=3):
    length = 400
    text_snippet = []
    if len(hit.bytes) >= samples:
        byte_sample = sample(hit.bytes, samples)
    else:
        byte_sample = hit.bytes
    for byte in byte_sample: 
        byte = [int(byte)]
        bytes, byte_start = adjust_bytes(byte, length)
        print >> sys.stderr, "PATH", path
        conc_text = f.get_text(hit, byte_start, length, path)
        conc_start, conc_middle, conc_end = chunkifier(conc_text, bytes, highlight=True, kwic=kwic)
        conc_start = clean_text(conc_start, kwic=kwic)
        conc_end = clean_text(conc_end, kwic=kwic)
        if kwic:
            conc_middle = clean_text(conc_middle, notag=False, kwic=kwic)
            conc_text = (conc_start + conc_middle + conc_end).decode('utf-8', 'ignore')
            conc_text = align_text(conc_text, 1)
        else:
            conc_text = (conc_start + conc_middle + conc_end).decode('utf-8', 'ignore')
        text_snippet.append(conc_text)
    if kwic:
        text = '<br>\n'.join(text_snippet)
    else:
        text = '... '.join(text_snippet)
    return text
    
     
