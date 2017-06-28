import json, requests, uuid

DAEMON_URL = 'http://13.90.96.240:8088/v2'
WALLET_URL = 'http://13.90.96.240:8089/v2'

class json_rpc:
    def __init__(self):
        self.counter = -1

    def encode(self, method, params):
        self.counter += 1
        return json.dumps({
            'jsonrpc': '2.0',
            'id': self.counter,
            'method': method,
            'params': params
        })

    def decode(self, message):
        return json.loads(message)['result']

RPC = json_rpc()

def make_wallets():
    '''Creates factoid and entry credit wallets on the server and returns a tuple of the addresses.'''
    
    factoid_request = requests.post(
        url=WALLET_URL,
        data=RPC.encode('generate-factoid-address'),
    )

    ec_request =  requests.post(
        url=WALLET_URL,
        data=RPC.encode('generate-ec-address'),
    )

    return (RPC.decode(factoid_request.text)['public'],
            RPC.decode(ec_request.text)['public'])

def buy_entry_credits(factoid_address, ec_address):
    '''Deposits entry credits in ec_address using all the funds from factoid_address'''

    # Get the balance of factoid_address (in Factoshis = Factoids * 10e8)
    balance_request = requests.get(
        url=DAEMON_URL,
        data=RPC.encode('factoid-balance', {'address': factoid_address})
    )
    balance = RPC.decode(balance_request.text)['balance']

    # Get the current transaction fee
    # Get a unique transaction name
    TX_NAME = uuid.uuid4().hex
    
    # Start a new transaction
    requests.post(
        url=WALLET_URL,
        data=RPC.encode('new-transaction', tx_name = TX_NAME)
    )

    # Add funds from our factoid address
    requests.post(
        url=WALLET_URL,
        data=RPC.encode('add-input', {'tx-name': TX_NAME,
                                      'address': factoid_address,
                                      'amount': balance})
    )
    

print(make_wallets())
