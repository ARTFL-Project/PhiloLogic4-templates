#!/usr/bin/env python
import sys
import re
from format import adjust_bytes, chunkifier, clean_text
from get_text import get_text

def concordance(hit, path, q, length=400):
    bytes, byte_start = adjust_bytes(hit.bytes, length)
    conc_text = get_text(hit, byte_start, length, path)
    conc_start, conc_middle, conc_end = chunkifier(conc_text, bytes, highlight=True)
    conc_start = clean_text(conc_start)
    conc_end = clean_text(conc_end)
    conc_text = conc_start + conc_middle + conc_end
    return conc_text.decode('utf-8', 'ignore')
    
