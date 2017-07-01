from hashlib import sha256
import redis, json, requests, time

SERVER_URL = 'http://13.90.154.24:8089'

config = json.loads(requests.get(SERVER_URL + '/config/').text)

database = redis.StrictRedis(host=config['redis']['ip'],
                             port=config['redis']['port'],
                             password=config['redis']['pass'])

USERNAME = config['tierion']['user']
PASSWORD = config['tierion']['pass']

HEADERS, AUTH_TIMEOUT = None, 0

def _set_headers():
    global HEADERS, AUTH_TIMEOUT

    auth_response = json.loads(requests.post(
        url='https://hashapi.tierion.com/v1/auth/token',
        data=json.dumps({
            'username': config['tierion']['user'],
            'password': config['tierion']['pass']
        }),
        headers={'content-type': 'application/json'}
    ).text)
    
    token = auth_response['access_token']
    timeout = time.time() + auth_response['expires_in'] - 100
    
    headers = {
        'Authorization': 'Bearer ' + token,
        'content-type': 'application/json'
    }

    HEADERS, AUTH_TIMEOUT = headers, timeout


def notarize(data):
    '''Notarize the bytes object *data* in the bitcoin blockchain and store the certificate in Redis.'''

    if type(data) != bytes:
        raise ValueError('Cannot hash non-bytes data! Convert your data to bytes and try again.')
    digest = sha256(data).hexdigest()
    
    if time.time() > AUTH_TIMEOUT: _set_headers()

    submitHashURL = 'https://hashapi.tierion.com/v1/hashitems'
    receiptId = json.loads(requests.post(
        url=submitHashURL,
        data=json.dumps({'hash': digest}),
        headers=HEADERS
    ).text)['receiptId']

    callback_url = SERVER_URL + '/api/' + ''.join(['?digest=',
                                                   digest,
                                                   '&receiptId=',
                                                   receiptId])
    
    createBlockSubscriptionURL = 'https://hashapi.tierion.com/v1/blocksubscriptions'    
    response = json.loads(requests.post(
        url=createBlockSubscriptionURL,
        data=json.dumps({
            'callbackUrl': callback_url,
            'label': receiptId
        }),
        headers=HEADERS
    ).text)
    
    try:
        response['id']
    except KeyError:
        raise RuntimeError('Hash submission failed!')
    
def verify(data):
    '''Query Redis to get a receipt with which the notarization of the bytes object *data* can be verified.'''

    if type(data) != bytes:
        raise ValueError('Cannot hash non-bytes data! Convert your data to bytes and try again.')

    digest = sha256(data).hexdigest()
    return database.get(digest)
