#!/usr/bin/env python

import sqlite3
import sys

obj_dict = {'doc': 1, 'div1': 2, 'div2': 3, 'div3': 4, 
            'para': 5, 'sent': 6, 'word': 7}
            

class ir_hit_wrapper(object):
    
    def __init__(self, db,hit, bytes, score, obj_type=False, encoding='utf-8'):
        self.db = db.dbh.cursor()
        self.toms_table = set(db.locals["metadata_fields"] + ['word_count', 'filename'])
        self.rr_table_name = db.locals['ranked_relevance_table_name']
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
        if field == "filename":
            self.hit = self.hit[:1] + ' 0 0 0 0 0 0'
        try:
            if field in self.toms_table:
                table = 'toms'
            else:
                table = self.rr_table_name
            query = 'select %s from %s where philo_id=? limit 1' % (field, table)
            print >> sys.stderr, query, self.hit
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
    
    def __init__(self, sqlhits, db):
        self.sqlhits = sqlhits
        self.db = db
        self.done = True
    
    def __getitem__(self,n):
        if isinstance(n,slice):
            hits = self.sqlhits[n]
            return [ir_hit_wrapper(self.db,philo_id, hit['bytes'], hit['tf_idf'], obj_type=hit['obj_type']) for philo_id, hit in hits]
    
    def __iter__(self):
        for philo_id, hit in self.sqlhits:
            yield ir_hit_wrapper(self.db,philo_id, hit['bytes'], hit['tf_idf'], obj_type=hit['obj_type'])
        
    def __len__(self):
        return len(self.sqlhits)
