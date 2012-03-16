#!/usr/bin/env python

import sqlite3
from HitWrapper import *
import sys

obj_dict = {'doc': 1, 'div1': 2, 'div2': 3, 'div3': 4, 
            'para': 5, 'sent': 6, 'word': 7}
            

class ir_hit_wrapper(object):
    
    def __init__(self, hit, bytes, db, score, path, obj_type=False, encoding='utf-8'):
        self.toms_db = db
        self.db = sqlite3.connect(path + '/data/' + obj_type + '_word_counts.db')
        self.path = path
        self.hit = hit
        self.bytes = bytes
        self.type = obj_type
        self.encoding = encoding
        self.toms = object_wrapper(hit, bytes, self.toms_db, obj_type=obj_type)
        self.score = score
        print >> sys.stderr, self.score
        
    def __getitem__(self, key):
        return getattr(self.toms, key)
        
    def __getattr__(self, name):
        return getattr(self.toms, name)
        

class ir_results_wrapper(object):
    
    def __init__(self, sqlhits, db, path):
        self.db = db
        self.sqlhits = sqlhits
        self.path = path
    
    def __getitem__(self,n):
        if isinstance(n,slice):
            hits = self.sqlhits[n]
            return [ir_hit_wrapper(philo_id.split(), bytes, self.db, tf_idf, self.path, obj_type=obj_type) for philo_id, obj_type, bytes, tf_idf in hits]
    
    def __iter__(self):
        for philo_id, obj_type, bytes, tf_idf in self.sqlhits:
            hit_id = philo_id.split()
            yield ir_hit_wrapper(hit_id, bytes, self.db, tf_idf, self.path, obj_type=obj_type)
        
    def __len__(self):
        return len(self.sqlhits)
