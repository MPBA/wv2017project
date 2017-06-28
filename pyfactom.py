import json, requests, uuid

DAEMON_URL = 'http://13.90.96.240:8088/v2'
WALLET_URL = 'http://13.90.96.240:8089/v2'

class json_rpc:
    def __init__(self):
        self.counter = -1

    def encode(self, method, params=''):
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

def buy_entry_credits(factoid_address, ec_address, amount=None):
    '''
    Deposits entry credits in ec_address using funds from factoid_address. 
    If amount is None, use all the funds, else use amount * 10e8 Factoids.
    If factoid_address does not have enough factoids, IOError will be raised.
    '''

    # Get the balance of factoid_address (in Factoshis = Factoids * 10e8) if amount is None
    if amount == None:
        balance_request = requests.push(
            url=DAEMON_URL,
            data=RPC.encode('factoid-balance', {'address': factoid_address})
        )
        balance = RPC.decode(balance_request.text)['balance']
    else:
        balance = amount
        
    # Get a unique transaction name
    TX_NAME = uuid.uuid4().hex[:30]

    # Start a new transaction
    res = requests.post(
        url=WALLET_URL,
        data=RPC.encode('new-transaction', {'tx-name': TX_NAME})
    )

    # Add all funds from our factoid address as an input
    res = requests.post(
        url=WALLET_URL,
        data=RPC.encode('add-input', {'tx-name': TX_NAME,
                                      'address': factoid_address,
                                      'amount': balance})
    )

    # Route the entire input to the entry credit output
    res = requests.post(
        url=WALLET_URL,
        data=RPC.encode('add-ec-output', {'tx-name': TX_NAME,
                                          'address': ec_address,
                                          'amount': balance})
    )

    # Specify that the transaction fee should be subtracted from the entry credit output
    res = requests.post(
        url=WALLET_URL,
        data=RPC.encode('sub-fee', {'tx-name': TX_NAME,
                                    'address': ec_address})
    )

    # Sign the transaction
    res = requests.post(
        url=WALLET_URL,
        data=RPC.encode('sign-transaction', {'tx-name': TX_NAME})
    )

    # Get the hex for the transaction
    compose_request = requests.post(
        url=WALLET_URL,
        data=RPC.encode('compose-transaction', {'tx-name': TX_NAME})
    )

    transaction_hex = RPC.decode(compose_request.text)['params']['transaction']

    # Submit the transaction to the network using factoid-submit
    submit_request = requests.post(
        url=DAEMON_URL,
        data=RPC.encode('factoid-submit', {'transaction': transaction_hex})
    )
    response = RPC.decode(submit_request.text)
    print(response)
    if response != 'Successfully submitted the transaction':
        raise IOError('Transaction submission failed!')

    
buy_entry_credits('FA3bNrrt7F34ANPDnRdQESRhN3SD3MQJqUZWdpbKGX2J66wxBFbP',
                  'EC1rV8ZrsscKmTA2K4CX3xQRPki2FM18E79MRoJuiAq9g4yGoFhB',
                  amount=100000)
 
