#!/usr/bin/env python

from __future__ import division
import sqlite3
from math import log
from format import adjust_bytes, chunkifier, clean_text
from get_text import get_text
import sys

def retrieve_hits(q, path):
    object_types = ['doc', 'div1', 'div2', 'div3', 'para', 'sent', 'word']
    obj_type = q['obj_type']
    depth = object_types.index(obj_type) + 1 ## this is for philo_id slices
    
    ## Open cursors for sqlite tables
    conn = sqlite3.connect(path + '/data/' + obj_type + '_word_counts.db')
    c = conn.cursor()
    toms_conn = sqlite3.connect(path + '/data/toms.db')
    toms_c = toms_conn.cursor()
    
    ## Get total number of objects
    toms_c.execute('select count(*) from toms where philo_type="%s"' % obj_type)
    total_docs = int(toms_c.fetchone()[0])
    
    ## Filter out if necessary
    philo_ids = []
    for field in q['metadata']:
        if field != 'n' and q['metadata'][field] != '':
            query = 'select philo_id from toms where %s=?' % field
            toms_c.execute(query, (q['metadata'][field],))
            results = [i[0].split()[0] for i in toms_c.fetchall()] ## just keep doc id
            print >> sys.stderr, results
            philo_ids.extend(results)
    if philo_ids:
        philo_ids = set(philo_ids)
        print >> sys.stderr, philo_ids
    
    ## Compute IDF
    c.execute('select count(*) from toms where philo_name=?', (q['q'],))
    docs_with_word = int(c.fetchone()[0]) or 1  ## avoid division by 0
    doc_freq = total_docs / docs_with_word
    if doc_freq == 1:
        doc_freq = (total_docs + 1) / docs_with_word ## The logarithm won't be equal to 0
    idf = log(doc_freq)
    
    query = 'select philo_id, %s_token_count, byte_start from toms where philo_name=?' % obj_type
    c.execute(query, (q['q'],))
    new_results = []
    for philo_id, token_counts, byte_start in c.fetchall():
        doc_id = philo_id.split()[0]
        #print >> sys.stderr, doc_id
        if not philo_ids or doc_id in philo_ids:
            obj_id = ' '.join(philo_id[0].split()[:depth]) 
            obj_id = obj_id + ' ' + ' '.join('0' for i in range(7 - depth))
            toms_c.execute('select word_count from toms where philo_id=?', (obj_id,))
            total_word_count = int(toms_c.fetchone()[0])
            term_frequency = token_counts/total_word_count
            tf_idf = term_frequency * idf
            new_results.append((philo_id, obj_type, byte_start.split(), tf_idf))
    return sorted(new_results, key=lambda x: x[3], reverse=True)
 
def relevance(hit, path, q):
    length = 100
    text_snippet = []
    for byte in hit.bytes[:4]:
        byte = [int(byte)]
        bytes, byte_start = adjust_bytes(byte, length)
        conc_text = get_text(hit, byte_start, length, path)
        conc_start, conc_middle, conc_end = chunkifier(conc_text, bytes, highlight=True)
        conc_start = clean_text(conc_start)
        conc_end = clean_text(conc_end)
        conc_text = conc_start + conc_middle + conc_end
        text_snippet.append(conc_text)
    return '...'.join(text_snippet).decode('utf-8', 'ignore')
    
     