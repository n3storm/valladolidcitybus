# -*- coding: utf-8 -*-
from hashlib import sha1
import time
import pickle
import os
from werkzeug.contrib.cache import SimpleCache
from flask import request

CACHE_TIMEOUT = 60 * 100

cache = SimpleCache()

class cached(object):

    def __init__(self, timeout=None):
        self.timeout = timeout or CACHE_TIMEOUT

    def __call__(self, f):
        def decorator(*args, **kwargs):
            response = cache.get(request.path)
            if response is None:
                response = f(*args, **kwargs)
                cache.set(request.path, response, self.timeout)
            return response
        return decorator

def cache_disk(seconds = 30, cache_folder="/tmp"):  
    def doCache(f):  
        def inner_function(*args, **kwargs):  
  
            # calculate a cache key based on the decorated method signature  
            key = sha1(str(f.__module__) + str(f.__name__) + str(args) + str(kwargs)).hexdigest() + '.valladolidcitybus'  
            filepath = os.path.join(cache_folder, key)  
  
            # verify that the cached object exists and is less than $seconds old  
            if os.path.exists(filepath):  
                modified = os.path.getmtime(filepath)  
                age_seconds = time.time() - modified  
                if age_seconds < seconds:  
                    return pickle.load(open(filepath, "rb"))  
  
            # call the decorated function...  
            result = f(*args, **kwargs)  
  
            # ... and save the cached object for next time  
            pickle.dump(result, open(filepath, "wb"))  
  
            return result  
        return inner_function  
    return doCache
