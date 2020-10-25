import subprocess
import json
import os
from pprint import pprint
from constants import BTC, BTCTEST, ETH
from bit import PrivateKeyTestnet
from bit.network import NetworkAPI
from web3 import Web3, middleware, Account
from web3.gas_strategies.time_based import medium_gas_price_strategy
from web3.middleware import geth_poa_middleware

#connec to web3

w3 = Web3(Web3.HTTPProvider(os.getenv('WEB3_PROVIDER', 'http://localhost:8545')))

#allow the POA middleware

w3.middleware_onion.inject(geth_poa_middleware, layer=0)

# set the gas price strategy
w3.eth.setGasPriceStrategy(medium_gas_price_strategy)

mnemonic = os.getenv("MNEMONIC", "large measure nut busy unable come buzz market universe normal one rabbit rule teach suspect")

# Deriving the wallet keys

def derive_wallets(coin=BTC,mnemonic=mnemonic, depth=3):

     command = f'./derive -g --mnemonic="{mnemonic}" --coin="{coin}" --numderive="{depth}" --format=json'

     p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
     (output, err) = p.communicate()
     p_status = p.wait()

     #wallet_keys = json.loads(output)

     return json.loads(output)


# Linking the transaction signing libraries

def priv_key_to_account(coin, priv_key):
    if coin == BTCTEST :
         return PrivateKeyTestnet(priv_key)
    elif coin ==ETH:
         return Account.privateKeyToAccount(priv_key)
    else:
         return ValueError('Incorrect coin code')


def create_tx(coin, account, to, amount):
    if coin == BTCTEST :
         return PrivateKeyTestnet.prepare_transaction(account.address, [(to, amount, BTC)])
    elif coin ==ETH:
         value = w3.toWei(amount, "ether")
         gastEstimate = w3.eth.estimateGas({"to": to, "from": account.address, "amount": value})
         return {
              "to": to,
              "from": account.address,
              "value": value,
              "gas": gasEstimate,
              "gasPrice": w3.eth.generateGasPrice(),
              "nonce": w3.eth.getTransactionCount(account.address),
              "chainId": we.net.chainId
         }
    else:
         return ValueError('Incorrect coin code')


def send_tx(coin, account, to, amount):
    if coin == BTCTEST :
         raw_tx = create_tx(coin, account, to, amount)
         signed = account.sign_transaction(raw_tx)
         return  NetworkAPI.broadcast_tx_testnet(signed)
    elif coin ==ETH:
         raw_tx = create_tx(coin, account, to, amount)
         signed = account.signTransaction(raw_tx)
         return w3.eth.sendRawTransaction(signed.rawTransaction)
    else:
         return ValueError('Incorrect coin code')


coins = {
     ETH: derive_wallets(coin=ETH),
     'BTCTEST': derive_wallets(coin=BTCTEST),
}

pprint(coins)

# Send transactions!

# Bitcoin transaction


btc_pk = coins['BTCTEST'][0]['privkey']

btc_key = priv_key_to_account(BTCTEST, btc_pk)
btc_trx = create_tx(BTCTEST, btc_key, 'mkfBAYL16aj8DyGBtrnBeCvJcRdUGQ2qEV', 0.000001)

btc_trx

send_tx(BTCTEST, btc_key, 'mkfBAYL16aj8DyGBtrnBeCvJcRdUGQ2qEV', 0.000001)


# Ethereium transaction


eth_pk = coins['eth'][0]['privkey']
eth_key = priv_key_to_account(ETH, eth_pk)

# Create transaction
eth_trx = create_tx(ETH, eth_key, '0x617437699df36E772dFbA7bE0ca9e0cA35d47b51', 20)
eth_trx

# Send transaction
send_tx(ETH, eth_key, '0x617437699df36E772dFbA7bE0ca9e0cA35d47b51', 20)