# In the name of GOD

from logging import Handler
from datetime import datetime
import time
import json

from elasticsearch import Elasticsearch


class LogSender:
    def __init__(self, elk) -> None:
        self.elk = elk

    def writelog(self, message, formatter, db_name=None) :
        index_name = db_name or f'log_{time.strftime("%Y_%m_%d")}'
        timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        log_data = {'message' : formatter(message)}
        log_data['timestamp'] = timestamp
        log_data['level'] = message.levelname
        print("<>"*20, " in elasticsearch write log ", "<>"*20)
        self.elk.index(index=index_name, document=log_data)
        print("<>"*20, f" index name: {index_name} ", "<>"*20)
        

class ElasticHandler(Handler) :
    def __init__(self, host,*args, **kwargs) :
        self.db_name = kwargs.pop('db_name', None)
        super().__init__(*args, **kwargs)
        self.host = host
        # self.formatter = kwargs.get('formatter')
        self.elk = Elasticsearch(self.host)
        self.sender = LogSender(elk=self.elk)

    def emit(self, record) :
        try:
            self.sender.writelog(record, self.format, db_name=self.db_name)
        except RecursionError:
            raise
        except Exception:
            self.handleError(record)
