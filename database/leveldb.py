import plyvel
import json
from pysyncobj import SyncObj, replicated

class Database(SyncObj):
    def __init__(self, port, part, primary, secundary):
        super(Database, self).__init__(primary, secundary)
        self.database = f'database/leveldb/{part}/{port}'
        
    @replicated
    def insertData(self, key, value): 
        db = plyvel.DB(self.database, create_if_missing=True)        
        bytesKey = bytes(key, 'utf-8')            
        bytesValue = bytes(json.dumps(value),'utf-8')
        db.put(bytesKey, bytesValue)
        db.close()
        
    @replicated
    def deleteData(self, key):
        db = plyvel.DB(self.database, create_if_missing=True)
        bytesKey = bytes(key, 'utf-8')
        db.delete(bytesKey)
        db.close()

    def getData(self, key):
        db = plyvel.DB(self.database, create_if_missing=True)
        bytesKey = bytes(key, 'utf-8')
        respBytes = db.get(bytesKey)
        resp = '' if not respBytes else respBytes.decode()
        db.close()
        return resp