from OP_RETURN import OP_RETURN_store
from hashlib import sha256
import redis, json

config = json.load(open('config.json'))
database = redis.StrictRedis(host=config['redis']['ip'], port=config['redis']['port'], db=0)

def notarize(data):
    '''Notarize the bytes object *data* in the bitcoin blockchain and store the TXID in Redis.'''
    
    if type(data) != bytes:
        raise ValueError('Cannot hash non-bytes data! Convert your data to bytes and try again.')

    digest = sha256(data).hexdigest()
    message = ('Notarized hash: ' + digest).encode('ascii')
    result = OP_RETURN_store(message)
    database.set(digest, result['txids'][0])

def get_txid(data):
    '''Query Redis to get the TXID at which the bytes object *data* is notarized.'''

    if type(data) != bytes:
        raise ValueError('Cannot hash non-bytes data! Convert your data to bytes and try again.')

    digest = sha256(data).hexdigest()
    return database.get(digest)
