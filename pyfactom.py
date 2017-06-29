import json, requests, uuid, time, hashlib

DAEMON_URL = 'http://13.90.96.240:8088/v2'
WALLET_URL = 'http://13.90.96.240:8089/v2'

FACTOID_ADDRESS = 'FA3bNrrt7F34ANPDnRdQESRhN3SD3MQJqUZWdpbKGX2J66wxBFbP'
EC_ADDRESS = 'EC1rV8ZrsscKmTA2K4CX3xQRPki2FM18E79MRoJuiAq9g4yGoFhB'


def encode(method, params=''):
    return json.dumps({
        'jsonrpc': '2.0',
        'id': uuid.uuid4().hex[:30],
        'method': method,
        'params': params
    })


def decode(message):
    return json.loads(message)['result']


def make_wallets():
    '''Creates factoid and entry credit wallets on the server and returns a tuple of the addresses.'''

    factoid_request = requests.post(
        url=WALLET_URL,
        data=encode('generate-factoid-address'),
    )

    ec_request = requests.post(
        url=WALLET_URL,
        data=encode('generate-ec-address'),
    )

    return (decode(factoid_request.text)['public'],
            decode(ec_request.text)['public'])


def buy_entry_credits(factoid_address, ec_address, amount=None):
    '''
    Deposits entry credits in ec_address using funds from factoid_address.
    If amount is None, use all the funds, else use amount * 10e8 Factoids.
    '''

    fee = 10**5

    # Get the balance of factoid_address (in Factoshis = Factoids * 10e8) if amount is None
    if amount == None:
        balance_request = requests.post(
            url=DAEMON_URL,
            data=encode('factoid-balance', {'address': factoid_address})
        )
        balance = decode(balance_request.text)['balance']
        amount = max(balance - fee, 0)
    else:
        amount = max(amount - fee, 0)

    # Get a unique transaction name
    TX_NAME = uuid.uuid4().hex[:30]

    # Start a new transaction
    res = requests.post(
        url=WALLET_URL,
        data=encode('new-transaction', {'tx-name': TX_NAME})
    )

    # Add all funds from our factoid address as an input
    res = requests.post(
        url=WALLET_URL,
        data=encode('add-input', {'tx-name': TX_NAME,
                                  'address': factoid_address,
                                  'amount': amount})
    )

    # Route the entire input to the entry credit output
    res = requests.post(
        url=WALLET_URL,
        data=encode('add-ec-output', {'tx-name': TX_NAME,
                                      'address': ec_address,
                                      'amount': amount})
    )

    # Specify that the transaction fee should be subtracted from the entry credit output
    res = requests.post(
        url=WALLET_URL,
        data=encode('add-fee', {'tx-name': TX_NAME,
                                'address': factoid_address})
    )

    # Sign the transaction
    res = requests.post(
        url=WALLET_URL,
        data=encode('sign-transaction', {'tx-name': TX_NAME})
    )

    # Get the hex for the transaction
    compose_request = requests.post(
        url=WALLET_URL,
        data=encode('compose-transaction', {'tx-name': TX_NAME})
    )

    transaction_hex = decode(compose_request.text)['params']['transaction']

    # Submit the transaction to the network using factoid-submit
    submit_request = requests.post(
        url=DAEMON_URL,
        data=encode('factoid-submit', {'transaction': transaction_hex})
    )
    response = decode(submit_request.text)['message']


def chain_id(extids):
    hs = hashlib.sha256()
    
    for id in map(lambda s: s.encode('utf-8'), extids):
        h = hashlib.sha256()
        h.update(id)
        hs.update(h.digest())
                  
    return hs.hexdigest()

def new_chain(ec_address):
    # Composing the chain
    extid = uuid.uuid4().hex
    extids = [extid[i:i+4] for i in range(0, len(extid), 4)]
    compose_chain = requests.post(
        url=WALLET_URL,
        data=encode('compose-chain',
                    {
                        'chain': {
                            'firstentry': {
                                "extids": extids,
                                "content": ''
                            }
                        },
                        "ecpub": ec_address,
                    }
        )
    )

    response = decode(compose_chain.text)
    commit_params, reveal_params = response['commit']['params'], response['reveal']['params']

    # Commiting the chain
    commit_chain = requests.post(
        url=DAEMON_URL,
        data=encode("commit-chain", commit_params)
            )

    response = decode(commit_chain.text)

    # Reveal the chain
    reveal_chain = requests.post(
        url=DAEMON_URL,
        data=encode("reveal-chain", reveal_params)
            )
    response = decode(reveal_chain.text)

    # Return the calculated ChainID
    return chain_id(extids)

print(new_chain(EC_ADDRESS))
#buy_entry_credits(FACTOID_ADDRESS, EC_ADDRESS, amount=100000)
