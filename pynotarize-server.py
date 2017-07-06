from flask import Flask, request
import requests, json, redis
app = Flask(__name__)

config = json.load(open('config.json'))

database = redis.StrictRedis(host='localhost',
                             port=config['redis']['port'],
                             password=config['redis']['pass'])

@app.route('/config/')
def send_config():
    return json.dumps(config)

@app.route('/api/', methods=['POST'])
def store_receipt():
    # Get an auth token using the user and pass
    auth_response = json.loads(requests.post(
        url='https://hashapi.tierion.com/v1/auth/token',
        data=json.dumps({
            'username': config['tierion']['user'],
            'password': config['tierion']['pass']
        }),
        headers={'content-type': 'application/json'}
    ).text)
    token = auth_response['access_token']
    
    # Get the receipt for the digest using the receiptId
    receiptURL = 'https://hashapi.tierion.com/v1/receipts/' + request.args['receiptId']
    receipt = json.loads(requests.get(
        url=receiptURL,
        headers = {
            'Authorization': 'Bearer ' + token,
            'content-type': 'application/json'
        }
    ).text)['receipt']

    # Store (digest, receipt) in the database
    database.set(request.args['digest'], receipt)

    # Unsubscribe from notifications about this receipt
    deleteURL = 'https://hashapi.tierion.com/v1/blocksubscriptions/' + request.args['receiptId']
    requests.delete(url=deleteURL,
                    headers = {
                        'Authorization': 'Bearer ' + token,
                        'content-type': 'application/json'
                    })
    
    return ''
