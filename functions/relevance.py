#!/usr/bin/env python

from __future__ import division
import sqlite3
from math import log
from format import adjust_bytes, chunkifier, clean_text, align_text
from get_text import get_text
import sys

def retrieve_hits(q, path):
    object_types = ['doc', 'div1', 'div2', 'div3', 'para', 'sent', 'word']
    obj_type = q['obj_type']
    depth = object_types.index(obj_type) + 1 ## this is for philo_id slices
    
    ## Open cursors for sqlite tables
    conn = sqlite3.connect(path + '/data/' + obj_type + '_word_counts.db')
    conn.text_factory = str
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
            philo_ids.extend(results)
    if philo_ids:
        philo_ids = set(philo_ids)
    
    query_words = q['q'].replace('|', ' ') ## Handle ORs from crapser
    q['q'] = q['q'].replace(' ', '|') ## Add ORs for search links
    
    ## Compute IDF
    idfs = {}
    if len(query_words.split()) > 1:
        for word in query_words.split():
            c.execute('select count(*) from toms where philo_name=?', (word,))
            docs_with_word = int(c.fetchone()[0]) or 1  ## avoid division by 0
            doc_freq = total_docs / docs_with_word
            if doc_freq == 1:
                doc_freq = (total_docs + 1) / docs_with_word ## The logarithm won't be equal to 0
            idf = log(doc_freq)
            idfs[word] = idf
    else:
        c.execute('select count(*) from toms where philo_name=?', (query_words,))
        docs_with_word = int(c.fetchone()[0]) or 1  ## avoid division by 0
        doc_freq = total_docs / docs_with_word
        if doc_freq == 1:
            doc_freq = (total_docs + 1) / docs_with_word ## The logarithm won't be equal to 0
        idf = log(doc_freq)
        idfs[query_words] = idf
    
    ## Construct query
    if len(query_words.split()) > 1:
        query = 'select philo_id, philo_name, %s_token_count, bytes, word_count from toms where ' % obj_type
        words =  query_words.split()
        query += ' or '.join(['philo_name=?' for i in words])
        c.execute(query, words)
    else:
        query = 'select philo_id, philo_name, %s_token_count, bytes, word_count from toms where philo_name=?' % obj_type
        c.execute(query, (query_words,))
    
    ## TODO: implement multiple word query search
    new_results = {}
    for philo_id, philo_name, token_counts, bytes, word_count in c.fetchall():
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
            new_results[philo_id]['tf_idf'] += tf_idf
            new_results[philo_id]['bytes'].extend(bytes.split()) 
    return sorted(new_results.iteritems(), key=lambda x: x[1]['tf_idf'], reverse=True)
 
def relevance(hit, path, q, kwic=True):
    length = 400
    text_snippet = []
    for byte in hit.bytes[:4]:
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
    
     