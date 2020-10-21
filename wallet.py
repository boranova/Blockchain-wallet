import subprocess
import json
import os
from constants import *


mnemonic = os.getenv('MNEMONIC', 'insert mnemonic here')

# Deriving the wallet keys

def derive_wallets(mnemonic: str, coin: str, numerative : int):

command = f'./derive -g --mnemonic="{mnemonic}" --coin="{coin}" --numderive="{numerative}" --cols=index,path,address,privkey,pubkey,pubkeyhash,xprv,xpub --format=json'

p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
(output, err) = p.communicate()

keys = json.loads(output)

return keys


# Linking the transaction signing libraries

def priv_key_to_account(coin, privkey):
    if coin == "BTCTEST" :
         return PrivateKeyTestnet(priv_key)
    elif coin =="ETH":
         return Account.privateKeyToAccount(priv_key)
    else:
        return ValueError('Incorrect coin code')


def create_tx(coin, account, to, amount):
    if coin == "BTCTEST" :
         return PrivateKeyTestnet.prepare_transaction(account.address, [(to, amount, BTC)])
    elif coin =="ETH":
         return ????????
    else:
        return ValueError('Incorrect coin code')


def send_tx(coin, account, to, amount):
    if coin == "BTCTEST" :
         return  NetworkAPI.broadcast_tx_testnet(signed)
    elif coin =="ETH":
         return w3.eth.sendRawTransaction(signed.rawTransaction)
    else:
        return ValueError('Incorrect coin code')

# Send transactions!
# Bitcoin transaction



# Ethereium transaction

