#!/usr/bin/env python

from __future__ import division
import sys
sys.path.append('..')
import functions as f
import sqlite3
from math import log
from random import sample
from functions.format import adjust_bytes, chunkifier, clean_text, align_text
from get_text import get_text
from bibliography import bibliography
import re
from render_template import render_template


def relevance(HitWrapper, IRHitWrapper, path, db, dbname, q, environ):
    if q['q'] == '':
        return bibliography(HitWrapper, q, db, dbname)
    else:
        hits = retrieve_hits(q, path)
        results = IRHitWrapper.ir_results_wrapper(hits,db,path)
    return render_template(results=results,db=db,dbname=dbname,q=q,fetch_relevance=fetch_relevance,f=f,format=format,
                                path=path, results_per_page=q['results_per_page'], template_name='relevance.mako')

def retrieve_hits(q, path):
    object_types = ['doc', 'div1', 'div2', 'div3', 'para', 'sent', 'word']
    obj_type = q['obj_type']
    depth = object_types.index(obj_type) + 1 ## this is for philo_id slices
    
    ## Open cursors for sqlite tables
    conn = sqlite3.connect(path + '/data/' + 'toms.db')
    conn.row_factory = sqlite3.Row
    conn.text_factory = str
    c = conn.cursor()
    toms_conn = sqlite3.connect(path + '/data/toms.db')
    toms_c = toms_conn.cursor()
    
    ## Filter out if necessary
    philo_ids = []
    for field in q['metadata']:
        if field != 'n' and q['metadata'][field] != '':
            query = 'select philo_id from toms where %s=? and philo_type=?' % field
            toms_c.execute(query, (q['metadata'][field], obj_type))
            results = [i[0].split()[0] for i in toms_c.fetchall()] ## just keep doc id
            philo_ids.extend(results)
    if philo_ids:
        philo_ids = set(philo_ids)
        total_docs = len(philo_ids)
    else:
        toms_c.execute('select count(*) from toms where philo_type="%s"' % obj_type)
        total_docs = int(toms_c.fetchone()[0])
    
    query_words = q['q'].replace('|', ' ') ## Handle ORs from crapser
    q['q'] = q['q'].replace(' ', '|') ## Add ORs for search links
    
    ## Compute IDF
    idfs = {}
    for word in query_words.split():
        c.execute('select count(*) from %s_word_counts where philo_name=?' % obj_type, (word,))
        docs_with_word = int(c.fetchone()[0]) or 1  ## avoid division by 0
        doc_freq = total_docs / docs_with_word
        if doc_freq == 1:
            doc_freq = (total_docs + 1) / docs_with_word ## The logarithm won't be equal to 0
        idf = log(doc_freq)
        idfs[word] = idf
    
    ## Construct query
    if len(query_words.split()) > 1:
        query = 'select * from %s_word_counts where ' % obj_type
        words =  query_words.split()
        query += ' or '.join(['philo_name=?' for i in words])
        c.execute(query, words)
    else:
        query = 'select * from %s_word_counts where philo_name=?' % obj_type
        c.execute(query, (query_words,))
    
    new_results = {}
    for i in c.fetchall():
        philo_id = i['philo_id']
        philo_name = i['philo_name']
        token_counts = i['doc_token_count']
        bytes = i['bytes']
        word_count = i['word_count']
        boost = metadata_boost(philo_name, q['metadata'], i)
        doc_id = philo_id.split()[0]
        if not philo_ids or doc_id in philo_ids:
            obj_id = ' '.join(philo_id[0].split()[:depth]) 
            obj_id = obj_id + ' ' + ' '.join('0' for i in range(7 - depth))
            total_word_count = int(word_count)
            term_frequency = token_counts/total_word_count
            tf_idf = term_frequency * idfs[philo_name]
            if philo_id not in new_results:
                new_results[philo_id] = {}
                new_results[philo_id]['obj_type'] = obj_type
                new_results[philo_id]['bytes'] = []
                new_results[philo_id]['tf_idf'] = 0
            new_results[philo_id]['tf_idf'] += tf_idf * boost
            new_results[philo_id]['bytes'].extend(bytes.split()) 
    return sorted(new_results.iteritems(), key=lambda x: x[1]['tf_idf'], reverse=True)
    
def metadata_boost(word, metadata, i):
    boost = 0
    for field in metadata:
        try:
            if re.search(word, i[field], re.I):
                boost += 4
        except (IndexError, TypeError):
            pass
    return boost or 1
 
def fetch_relevance(hit, path, q, kwic=True, samples=4):
    length = 400
    text_snippet = []
    if len(hit.bytes) >= samples:
        byte_sample = sample(hit.bytes, samples)
    else:
        byte_sample = hit.bytes
    for byte in byte_sample: 
        byte = [int(byte)]
        bytes, byte_start = adjust_bytes(byte, length)
        conc_text = get_text(hit, byte_start, length, path)
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
    
     
