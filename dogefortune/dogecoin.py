import json
import requests
from dogefortune import dogeconfig

# Set up dogecoin access
rpcauth = (dogeconfig.DOGECOIN_RPC_USER, dogeconfig.DOGECOIN_RPC_PASS)
rpcurl = dogeconfig.DOGECOIN_RPC_URL

# Globals r cool
last_block_hash = "0"
try:
    with open("last_block_hash", "r") as f:
        last_block_hash = f.read()
except IOError:
    pass


def dogerpc(method, args=None):
    if not args:
        args = []
    headers = {"Content-Type": "application/json"}
    payload = {"jsonrpc": "1.0", "id": "dogefortune",
               "method": method, "params": args}
    data = json.dumps(payload)
    req = requests.get(rpcurl, auth=rpcauth, headers=headers, data=data).json()
    return req['result']


def get_block_count():
    return dogerpc("getblockcount")


def get_transactions():
    global last_block_hash
    r = dogerpc("listsinceblock", [last_block_hash])
    last_block_hash = r['lastblock']
    try:
        with open("last_block_hash", "w") as f:
            f.write(last_block_hash)
    except IOError:
        pass
    return r['transactions']


def get_address(username):
    return dogerpc("getaccountaddress", [username])
