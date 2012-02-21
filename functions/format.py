#!/usr/bin/env python

import re
import htmlentitydefs
from BeautifulSoup import BeautifulSoup
from philologic.DirtyFormatter import Formatter
from custom_object_format import custom_format

def adjust_bytes(bytes, length):
    """Readjust byte offsets for concordance"""
    bytes = sorted(bytes) # bytes aren't stored in order
    byte_start = bytes[0] - (length / 2)
    first_hit =  length / 2
    if byte_start < 0:
        first_hit = first_hit + byte_start ## this is a subtraction really
        byte_start = 0
    new_bytes = []
    for pos, word_byte in enumerate(bytes):
        if pos == 0:
            new_bytes.append(first_hit)
        else:
            new_bytes.append(word_byte - byte_start)
    return new_bytes, byte_start


def chunkifier(conc_text, bytes, kwic=False, highlight=False):
    """Divides the passage in three:
    * from the beginning to the first hit (not included)
    * from the first hit to the end of the last hit
    * form the end of the last hit to the end of the passage
    Returns a tuple containing all three parts of the passage"""
    conc_start = conc_text[:bytes[0]]
    conc_middle = ''
    end_byte = int
    for pos, word_byte in enumerate(bytes):
        if highlight:
            text, end_byte = highlighter(conc_text, word_byte, kwic=kwic)
        else:
            text_chunks = re.split("([\w']+)", conc_text[word_byte:])
            end_byte = word_byte + len(text_chunks[1])
            text = text_chunks[1]
        try:
            conc_middle += text + conc_text[end_byte:bytes[pos+1]]
        except IndexError:
            conc_middle += text
    conc_end = conc_text[end_byte:]
    
    ## Make sure we have no words cut out
    conc_start = re.sub("^[^\s]* ", "", conc_start)
    conc_end = re.sub(" [^\s]*$", "", conc_end)
    
    return conc_start, conc_middle, conc_end


def highlighter(text, word_byte, kwic=False):
    """This function highlights a passage based on the hit's byte offset"""
    # the split returns an empty list if the word_byte goes beyond the text excerpt
    # which causes an index error on the following line
    unicode_str = re.compile("([\w']+)", re.UNICODE)
    text_chunks = unicode_str.split(text[word_byte:].decode('utf-8', 'ignore'))
    end_byte = word_byte + len(text_chunks[1].encode('utf-8', 'ignore'))
    if kwic:
        text = '<b>' + text_chunks[1].encode('utf-8', 'ignore') + '</b>' # 0 element is always an empty string
    else:
        text = '<span class="highlight">' + text_chunks[1].encode('utf-8', 'ignore') + '</span>' # 0 element is always an empty string
    return text, end_byte


def clean_text(text, notag=True, kwic=False, collocation=False):
    """Cleans your text, and by default removes all tags"""
    text = re.sub("^[^<]*?>","",text)
    text = re.sub("<[^>]*?$","",text)
    if notag:
        text = re.sub("<.*?>","",text)
    if kwic:
        text = text.replace('\n', ' ')
        text = text.replace('\r', '')
        text = text.replace('\t', ' ')
        ## Assuming that the highlight tag is <b>
        temp_text = re.sub('<(/?b)>', '[\\1]', text)
        temp_text = re.sub('<.*?>', '', temp_text)
        text = re.sub('\[(/?b)\]', '<\\1>', temp_text)
        text = re.sub(' {2,}', ' ', text)
    if collocation:
        text = re.sub("-", " ", text)
        text = re.sub("&dot;", " ", text)
        text = re.sub("&nbsp;", " ", text)
        text = re.sub("&amp;", " ", text)
        text = re.sub("&.aquo;", " ", text)
        text = re.sub("&.squo;", " ", text)
        text = re.sub("&ldquo;", " ", text)
        text = re.sub("&rdquo;", " ", text)
        text = re.sub("&.dash;", " ", text)
        text = re.sub("&lt;", " ", text)
        text = re.sub("&gt;", " ", text)
        text = re.sub("&hyphen;", " ", text)
        text = re.sub("&colon;", " ", text)
        text = re.sub("&excl;", " ", text)
        text = re.sub("\xe2\x80\x9c", "", text) ## ldquo
        text = re.sub("\xe2\x80\x9d", "", text) ## rdquo
        text = re.sub("\"", " ", text)
        text = re.sub(" +", " ", text)
        text = re.sub("^  *", "", text)
        text = re.sub("  *$", "", text)
        text = re.sub("[^a-zA-Z'\177-\344 ]", " ", text) ## getting rid of '&' and ';' from orig.##
        text = text.decode('utf-8', 'ignore')
    return text
  
  
def align_text(text, hit, chars=40):
    """This function is meant for formating text for KWIC results"""
    start_hit = text.index('<b>')
    end_hit = text.index('</b>') + 4
    tag_length = 7 * len(hit.bytes)
    start_text = convert_entities(text[:start_hit])
    if len(start_text) < chars:
        white_space = ' ' * (chars - len(start_text))
        start_text = white_space + start_text
    start_text = '<span style="white-space:pre-wrap;">' + start_text[-chars:] + '</span>'
    end_text = convert_entities(text[end_hit:])
    match = convert_entities(text[start_hit:end_hit])
    return start_text + match + end_text[:chars+tag_length]
   
    
def clean_word(word):
    """Removes any potential non-word characters"""
    word = re.sub("[0-9]* ", "", word)
    word = re.sub("[\s]*", "", word)
    word = word.replace('\n', '')
    word = word.replace('\r', '')
    return word


def tokenize_text(text):
    """Returns a list of individual tokens"""
    text = text.lower()
    text_tokens = re.split('[ ,;:?.!"]+', text) ## this splits on whitespaces and punctuation
    text_tokens = [clean_word(token) for token in text_tokens if token] ## remove empty strings
    return text_tokens
 
   
def fix_html(text):
    """Fixes broken HTML tags"""
    return unicode(BeautifulSoup(text))
 
def convert_entities(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)

def formatter(text):
    """This function calls an external script containing a dictionnary with formatting
    options for proper display in the web browser"""
    if custom_format():  ## check if the format dict contains any special formatting options
        f = Formatter(custom_format())
        return f.format(text)
    else:
        return text
