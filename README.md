`pynotarize` is a simple Python interface to the [Tierion](https://tierion.com/) blockchain notary service.

## Server setup
`pynotarize` depends on two services: `pynotarize-server` and Redis. A server-side `config.json` file provides password and port information to the client and the Tierion service. An example `config.json`, which should be in the same directory as `pynotarize-server.py`, is the following:

```json
{
    "tierion": {
        "user": "elliot.gorokhovsky@gmail.com",
        "pass": "webvalley2017"
    },

    "redis": {
        "ip": "13.90.154.24",
        "port": "8090",
        "pass": "EAx5QvAhfE"
    }
}
```
The `tierion` object contains Tierion account information, which is used to obtain an API key. The `redis` object contains information about how the client should access the database, which is used to save and retrieve the notary reciepts.

## Client setup
Once Redis and `pynotarize-server` are running on the server, simply set the `SERVER_URL` line of `pynotarize.py` with the IP and port of the `pynotarize-server` service. For example, if `pynotarize-server` is running on the server on port `8089`, we would set

```python
SERVER_URL = 'http://13.90.154.24:8089'
```

## Usage
To notarize a bytes object `s` in the Bitcoin blockchain, simply call

```
notarize(s)
```
This will store a SHA-256 hash of `s` in the blockchain in an upcoming block. Once the hash is included in a mined block (which takes 10 minutes on average), the Tierion service pushes a notification to the server containing the reciept of the notarization, which is stored in Redis.

To get the receipt for a bytes object `s` which has been notarized by `notarize(s)`, simply call
```
verify(s)
```
This will return a reciept in the open [Chainpoint](https://chainpoint.org/) format, which contains a path in the Merkle tree that Tierion used to notarize the hash of `s`, as well as information about how to find the tree in the blockchain. Chainpoint proofs are easy to verify using open-source tools, or even by hand, and prove beyond any reasonable doubt that `notarize(s)` was called at the timestamp indiciated in the reciept.