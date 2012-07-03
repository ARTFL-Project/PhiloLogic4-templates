#!/usr/bin/env python

import re
import sys
sys.path.append('../scripts/')
from scripts.crapser import *

def query_parser(query):
    query = query.lstrip().rstrip()
    if re.search('([A-Z]+|\*)', query):
        query = crapser(query)
    #query = query.decode('utf-8', 'ignore').lower().encode('utf-8', 'ignore')
    return query