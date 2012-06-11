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
    return render_template(results=hits,db=db,dbname=dbname,q=q,fetch_collocation=fetch_collocation,f=f,
                            path=path, results_per_page=q['results_per_page'], template_name='collocation.mako')

def fetch_collocation(results, path, q):

  ## set up filtering of most frequent 100 terms ##

    filter_list_path = path + '/data/WORK/all_frequencies'
    filter_words_file = open(filter_list_path)

    line_count = 0
    filter_list = set([])

    for line in filter_words_file:
        line = re.sub("[0-9]* ", "", line)
        line = re.sub("[\s]*", "", line)
        line = re.sub("\n", "", line)
        line_count = line_count + 1
        filter_list.add(line.decode('utf-8', 'ignore'))
        if line_count > 100:
                break
    
  ## start going though hits ##

    left_collocates = {}
    right_collocates = {}
    all_collocates = {}

     ## note:  combining the word lists and then creating dict ##
     ## for the total collocates. creating new dict/counts on  ##
     ## the fly (within individual for loops) gave odd results ##
     ## we'll revisit and try to create all_collocates along-  ##
     ## side the other two dicts for optimization....          ##

    for hit in results:
        left_word = []
        left_word = colloc_churner(hit, path, q, filter_list, left=True, right=False)
        left_plus_right = list(left_word)
        for l_word in left_word:
            if l_word in left_collocates:
                left_collocates[l_word] += 1
            else:
                left_collocates[l_word] = 1 
                

        right_word = []
        right_word = colloc_churner(hit, path, q, filter_list, left=False, right=True)
        for word in right_word:
            left_plus_right.append(word)
            if word in right_collocates:
                right_collocates[word] += 1
            else:
                right_collocates[word] = 1

        for lr_word in left_plus_right:
            if lr_word in all_collocates:
                all_collocates[lr_word] += 1
            else:
                all_collocates[lr_word] = 1
    

    left_out = sorted(left_collocates.items(), key=lambda x: x[1], reverse=True)
    right_out = sorted(right_collocates.items(), key=lambda x: x[1], reverse=True)
    all_out = sorted(all_collocates.items(), key=lambda x: x[1], reverse=True)

    tuple_out = zip(all_out, left_out, right_out)

    return tuple_out

def colloc_churner(hit, path, q, filter_list, length=400, highlighting=False, kwic=False, left=False, right=False):

    within_x_words = q['word_num']

    ## get my chunk of text ##
    bytes, byte_start = adjust_bytes(hit.bytes, length)
    conc_text = f.get_text(hit, byte_start, length, path)

    conc_left, conc_middle, conc_right = chunkifier(conc_text, bytes)

    ## left collocates ## 

    if left:
        conc_left = clean_text(conc_left, collocation=True)
        conc_left = conc_left.lower()
        conc_left = re.sub("^[^\s]* ", "", conc_left) ## hack off left-most word (potentially truncated)
        left_words = re.split("\s+", conc_left)

        left_words.reverse() ## left side needs to be reversed 

        left_words_to_pass = filter(left_words, filter_list, within_x_words)

        return left_words_to_pass

    ## right collocates ##

    if right:
        conc_right = clean_text(conc_right, collocation=True)
        conc_right = conc_right.lower()
        conc_right = re.sub(" [^\s]*$", "", conc_right) ## hack off right-most word (potentially truncated)
        right_words = re.split("\s+", conc_right)

        right_words_to_pass = filter(right_words, filter_list, within_x_words)

        return right_words_to_pass


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

