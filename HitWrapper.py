#!/usr/bin/python

import time
import sys
from itertools import islice

obj_dict = {'doc': 1, 'div1': 2, 'div2': 3, 'div3': 4, 
            'para': 5, 'sent': 6, 'word': 7}


class hit_wrapper(object):

    def __init__(self, hit, bytes, db, obj_type=False, encoding='utf-8'):
        self.db = db
        self.hit = hit
        self.bytes = bytes
        self.philo_id = hit
        self.encoding = encoding
        if obj_type:
            self.type = obj_type
        else:
            try:
                length = len(hit[:hit.index(0)])
            except ValueError:
                length = len(hit)
            self.type = [k for k in obj_dict if obj_dict[k] == length][0]

    def __getitem__(self, key):
        if key in obj_dict:
            return object_wrapper(self.hit, self.bytes, self.db, obj_type=key)
        else:
            return self.__metadata_lookup(key)
    
    def __getattr__(self, name):
        if name in obj_dict:
            return object_wrapper(self.hit, self.bytes, self.db, obj_type=name)
        else:
            return self.__metadata_lookup(name)
        
    def __metadata_lookup(self, field):
        width = 7
        philo_id = self.philo_id[:width]
        metadata = None
        while width:
            try:
                metadata = self.db[philo_id[:width]][field]
            except (TypeError,IndexError):
                ## if self.db[philo_id[:width]] returns None
                width -= 1
                continue
            if metadata != None:
                break
            width -= 1
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
 
           
class object_wrapper(object):
    
    def __init__(self, hit, bytes, db, obj_type=False, encoding='utf-8'):
        self.db = db
        self.hit = hit
        if obj_type:
            self.philo_id = hit[:obj_dict[obj_type]]
            self.type = obj_type
        else:
            self.philo_id = hit
            try:
                length = len(hit[:hit.index(0)])
            except ValueError:
                length = len(hit)
            self.type = [k for k in obj_dict if obj_dict[k] == length][0]
        self.bytes = bytes
        self.encoding = encoding
        

    def __getitem__(self, key):
        if key in obj_dict:
            return object_wrapper(self.hit, self.bytes, self.db, key)
        else:
            return self.__metadata_lookup(key)
        
    def __getattr__(self, name):
        if name in obj_dict:
            return object_wrapper(self.hit, self.bytes, self.db, name)
        else:
            return self.__metadata_lookup(name)
        
    def __metadata_lookup(self, field):
        metadata = None
        try:
            metadata = self.db[self.philo_id][field]
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

      
class results_wrapper(object):
    
    def __init__(self,hitlist,db):
        self.db = db
        self.hitlist = hitlist
        while not self.hitlist.done:
            time.sleep(.05)
            self.hitlist.update()

    def __getitem__(self,n):
        if isinstance(n,slice):
            hits = self.hitlist[n]
            return [hit_wrapper(hit,self.hitlist.get_bytes(hit),self.db, obj_type='hit') for hit in hits]
        hit = self.hitlist[n]
        return hit_wrapper(hit,self.hitlist.get_bytes(hit),self.db, obj_type='hit')
        
    def __len__(self):
        return len(self.hitlist)
       
       
class metadata_results_wrapper(object):
    
    def __init__(self, sqlhits, db):
        self.db = db
        self.sqlhits = list(sqlhits)


    def __iter__(self):
        for hit in self.sqlhits:
            hit_id = hit['philo_id'].split()
            byte = hit['byte_start']
            yield hit_wrapper(hit_id, byte, self.db, obj_type='metadata_hit')
        
    def __len__(self):
        return len(self.sqlhits)
