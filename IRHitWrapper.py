#!/usr/bin/env python

import sqlite3
from HitWrapper import *
import sys

obj_dict = {'doc': 1, 'div1': 2, 'div2': 3, 'div3': 4, 
            'para': 5, 'sent': 6, 'word': 7}
            

class ir_hit_wrapper(object):
    
    def __init__(self, hit, bytes, score, path, obj_type=False, encoding='utf-8'):
        conn = sqlite3.connect(path + '/data/' + 'toms.db')
        self.db = conn.cursor()
        self.hit = hit
        self.philo_id = hit.split()
        self.bytes = bytes
        self.type = obj_type
        self.encoding = encoding
        self.score = score
        
    def __getitem__(self, key):
        return self.__metadata_lookup(key)
        
    def __getattr__(self, name):
        return self.__metadata_lookup(name)
        
    def __metadata_lookup(self, field):
        metadata = None
        try:
            query = 'select %s from %s_word_counts where philo_id=? limit 1' % (field, self.type)
            self.db.execute(query, (self.hit, ))
            metadata = self.db.fetchone()[0]
        except (TypeError,IndexError):
            ## if self.db[self.philo_id[:width]] returns None]
            metadata = ''
        if metadata == None:
            metadata = ''
        if self.encoding:
            try:
                return metadata.decode(self.encoding, 'ignore')
            except AttributeError:
                ## if the metadata is an integer
                return metadata
        else:
            return metadata
        

class ir_results_wrapper(object):
    
    def __init__(self, sqlhits, db, path):
        self.sqlhits = sqlhits
        self.path = path
    
    def __getitem__(self,n):
        if isinstance(n,slice):
            hits = self.sqlhits[n]
            return [ir_hit_wrapper(philo_id, hit['bytes'], hit['tf_idf'], self.path, obj_type=hit['obj_type']) for philo_id, hit in hits]
    
    def __iter__(self):
        for philo_id, hit in self.sqlhits:
            yield ir_hit_wrapper(philo_id, hit['bytes'], hit['tf_idf'], self.path, obj_type=hit['obj_type'])
        
    def __len__(self):
        return len(self.sqlhits)
