#!/usr/bin/env python

def query_parser(query):
    query = query.lstrip().rstrip()
    query.decode('utf-8').lower().encode('utf-8')
    return query