from __future__ import with_statement

import logging
from celery.task import task
import PyV8

from openspending.model import Dataset

log = logging.getLogger(__name__)

def safe_strings(d):
    if isinstance(d, dict):
        return dict([(k, safe_strings(v)) for k,v in d.items()])
    elif isinstance(d, (list, tuple)):
        return [safe_strings(e) for e in d]
    elif isinstance(d, unicode):
        return d.encode('utf-8')
    return d

class Console(PyV8.JSClass):

    def log(self, message):
        log.info(message)

    def warn(self, message):
        log.warn(message)

    def error(self, message):
        log.error(message)

class Cursor(PyV8.JSClass):

    def __init__(self, it):
        self.it = it

    def next(self):
        try:
            return self.it.next()
        except StopIteration:
            return None

@task(ignore_result=True)
def mine(dataset_name, code):
    dataset = Dataset.by_name(dataset_name)
    
    class Global(PyV8.JSClass):

        def __init__(self):
            self.console = Console()
            self.dimensions = safe_strings(dataset.mapping)
            self.dataset = safe_strings(dataset.as_dict())

        def entries(self):
            try:
                return Cursor(dataset.entries())
            except Exception, e:
                print e

    try:
        with PyV8.JSContext(Global()) as ctxt:
            try:
                ctxt.enter()
                code = code.encode('utf-8')
                ctxt.eval(code)
            except Exception, e:
                log.error(e)
            finally:
                ctxt.leave()
    except Exception, e:
        log.error(e)
