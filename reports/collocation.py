#!/usr/bin/env python

import sys
sys.path.append('..')
import functions as f
import os
import re
from functions.wsgi_handler import wsgi_response
from render_template import render_template
from functions.format import adjust_bytes, clean_text, chunkifier
from bibliography import bibliography


def collocation(start_response, environ):
    db, dbname, path_components, q = wsgi_response(start_response, environ)
    path = os.getcwd().replace('functions/', '')
    if q['q'] == '':
        return bibliography(f,path, db, dbname,q,environ) ## the default should be an error message
    else:
        hits = db.query(q["q"],q["method"],q["arg"],**q["metadata"])
    return render_template(results=hits,db=db,dbname=dbname,q=q,fetch_collocation=fetch_collocation,link=link_to_concordance,
                           f=f,path=path, results_per_page=q['results_per_page'], template_name='collocation.mako')

def fetch_collocation(results, path, q, filter_words=100):
    within_x_words = q['word_num']    
    
    ## set up filtering of most frequent 100 terms ##
    filter_list_path = path + '/data/frequencies/word_frequencies'
    filter_words_file = open(filter_list_path)

    line_count = 0
    filter_list = set([])

    for line in filter_words_file:
        line_count += 1
        word = line.split()[0]
        filter_list.add(word.decode('utf-8', 'ignore'))
        if line_count > filter_words:
                break
    
    ## start going though hits ##
    left_collocates = {}
    right_collocates = {}
    all_collocates = {}
    
    count = 0
    for hit in results:
        ## get my chunk of text ##
        bytes, byte_start = adjust_bytes(hit.bytes, 400)
        conc_text = f.get_text(hit, byte_start, 400, path)
        conc_left, conc_middle, conc_right = chunkifier(conc_text, bytes)
        
        left_words = tokenize(conc_left, filter_list, within_x_words, 'left')
        if not sum([len(i) for i in left_words]):
            count += 1
        right_words = tokenize(conc_right, filter_list, within_x_words, 'right')
    
        for l_word in left_words:
            if l_word not in left_collocates:
                left_collocates[l_word] = 0
            left_collocates[l_word] += 1
            if l_word not in all_collocates:
                all_collocates[l_word] = 0
            all_collocates[l_word] += 1 

        for r_word in right_words:
            if r_word not in right_collocates:
                right_collocates[r_word] = 0
            if r_word not in all_collocates:
                all_collocates[r_word] = 0
            right_collocates[r_word] += 1
            all_collocates[r_word] += 1

    left_out = sorted(left_collocates.items(), key=lambda x: x[1], reverse=True)
    right_out = sorted(right_collocates.items(), key=lambda x: x[1], reverse=True)
    all_out = sorted(all_collocates.items(), key=lambda x: x[1], reverse=True)

    tuple_out = zip(all_out, left_out, right_out)
    print >> sys.stderr, "COUNT", count
    return tuple_out

def tokenize(text, filter_list, within_x_words, direction, highlighting=False):
    text = clean_text(text, collocation=True)
    text = text.lower()
    
    if direction == 'left':
        text = re.sub("^[^\s]* ", "", text) ## hack off left-most word (potentially truncated)
        word_list = re.split("\s+", text) 
        word_list.reverse() ## left side needs to be reversed
    else:
        text = re.sub(" [^\s]*$", "", text) ## hack off right-most word (potentially truncated)
        word_list = re.split("\s+", text)
        
    word_list = filter(word_list, filter_list, within_x_words)

    return word_list

def filter(word_list, filter_list, within_x_words):

    ## this code currently presumes filtering -- I append only non-filter words ##
    ## also, I check to make sure there are actual characters in my word -- no empties, please ##
    ## character set can be extended, of course ##

    words_to_pass = []

    for word in word_list:
        if word not in filter_list and re.search("[a-z\xa0-\xc3]", word):
            words_to_pass.append(word)
        if len(words_to_pass) == within_x_words:
            break
    return words_to_pass

def link_to_concordance(q, collocate, direction):
    collocate_values = [collocate, direction, q['word_num']]
    return f.link.make_query_link(q['q'], method=q['method'], arg=q['arg'], report="concordance_from_collocation",
                                  collocate=collocate_values,**q['metadata'])
    

