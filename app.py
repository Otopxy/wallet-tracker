from flask import Flask, render_template, request
import requests
import re
from datetime import datetime, timedelta

app = Flask(__name__)

# Replace with your API keys
ETHERSCAN_API_KEY = 'YourEtherscanAPIKey'
BSCSCAN_API_KEY = 'YourBSCScanAPIKey'
BLOCKCHAIR_API_KEY = 'YourBlockchairAPIKey'
SOLANA_API_URL = 'https://api.mainnet-beta.solana.com'
LITECOIN_API_URL = 'https://blockchair.com/litecoin/api/v1/address/'
DOGECOIN_API_URL = 'https://blockchair.com/dogecoin/api/v1/address/'

# List of known exchange wallet addresses
EXCHANGE_ADDRESSES = [
    '0x1234567890abcdef1234567890abcdef12345678',  # Example Binance wallet address
    '0xabcdefabcdefabcdefabcdefabcdefabcdefabcdef',  # Example Coinbase wallet address
    # Add more exchange addresses here...
]

def detect_blockchain(address):
    """Detect which blockchain the wallet address belongs to based on the address format."""
    if address.startswith('0x'):  # Ethereum / Binance Smart Chain
        return 'ethereum'
    elif address.startswith('1') or address.startswith('3') or address.startswith('bc1'):  # Bitcoin
        return 'bitcoin'
    elif len(address) == 32 and all(c in "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz" for c in address):  # Solana
        return 'solana'
    elif len(address) == 34 and address[0] == 'L':  # Litecoin (starts with L)
        return 'litecoin'
    elif len(address) == 34 and address[0] == 'D':  # Dogecoin (starts with D)
        return 'dogecoin'
    else:
        return 'unknown'

# Helper function to get the current time and subtract 7 days
def get_date_seven_days_ago():
    return datetime.utcnow() - timedelta(days=7)

def filter_transactions_by_date(transactions, blockchain):
    """Filter the transactions that are within the last 7 days."""
    seven_days_ago = get_date_seven_days_ago()
    filtered_transactions = []

    for tx in transactions:
        if blockchain == 'ethereum' or blockchain == 'bsc':
            timestamp = int(tx['timeStamp'])
            tx_date = datetime.utcfromtimestamp(timestamp)
        elif blockchain == 'bitcoin':
            timestamp = tx['time']
            tx_date = datetime.utcfromtimestamp(timestamp)
        elif blockchain == 'solana':
            timestamp = tx['blockTime']
            tx_date = datetime.utcfromtimestamp(timestamp)
        elif blockchain == 'litecoin':
            timestamp = tx['time']
            tx_date = datetime.utcfromtimestamp(timestamp)
        elif blockchain == 'dogecoin':
            timestamp = tx['time']
            tx_date = datetime.utcfromtimestamp(timestamp)
        else:
            continue
        
        if tx_date >= seven_days_ago:
            filtered_transactions.append(tx)

    return filtered_transactions

# Functions for different blockchains (with date filtering added)
def get_ethereum_transactions(address):
    url = f'https://api.etherscan.io/api?module=account&action=txlist&address={address}&startblock=0&endblock=latest&sort=desc&apikey={ETHERSCAN_API_KEY}'
    response = requests.get(url)
    data = response.json()
    if data['status'] == '1':
        return filter_transactions_by_date(data['result'], 'ethereum')
    return []

def get_bsc_transactions(address):
    url = f'https://api.bscscan.com/api?module=account&action=txlist&address={address}&startblock=0&endblock=latest&sort=desc&apikey={BSCSCAN_API_KEY}'
    response = requests.get(url)
    data = response.json()
    if data['status'] == '1':
        return filter_transactions_by_date(data['result'], 'bsc')
    return []

def get_bitcoin_transactions(address):
    url = f'https://api.blockchair.com/bitcoin/dashboards/address/{address}'
    response = requests.get(url)
    data = response.json()
    if 'data' in data:
        transactions = data['data'][address]['transactions']
        return filter_transactions_by_date(transactions, 'bitcoin')
    return []

def get_solana_transactions(address):
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getConfirmedSignaturesForAddress2",
        "params": [address, {"limit": 10}]
    }
    response = requests.post(SOLANA_API_URL, json=payload)
    data = response.json()
    if 'result' in data:
        return filter_transactions_by_date(data['result'], 'solana')
    return []

def get_litecoin_transactions(address):
    url = f'{LITECOIN_API_URL}{address}'
    response = requests.get(url)
    data = response.json()
    if 'data' in data:
        transactions = data['data'][address]['transactions']
        return filter_transactions_by_date(transactions, 'litecoin')
    return []

def get_dogecoin_transactions(address):
    url = f'{DOGECOIN_API_URL}{address}'
    response = requests.get(url)
    data = response.json()
    if 'data' in data:
        transactions = data['data'][address]['transactions']
        return filter_transactions_by_date(transactions, 'dogecoin')
    return []

def is_transaction_to_exchange(tx, blockchain):
    """Check if the transaction is sending funds to a known exchange address."""
    if blockchain in ['ethereum', 'bsc']:
        return tx['to'].lower() in (address.lower() for address in EXCHANGE_ADDRESSES)
    elif blockchain == 'bitcoin':
        # Bitcoin transactions will have a different structure; adapt as needed
        return False  # Placeholder for Bitcoin checks
    elif blockchain == 'solana':
        # Solana transaction checking logic (to be refined as needed)
        return False  # Placeholder for Solana checks
    elif blockchain == 'litecoin':
        # Litecoin transaction checking logic (to be refined as needed)
        return False  # Placeholder for Litecoin checks
    elif blockchain == 'dogecoin':
        # Dogecoin transaction checking logic (to be refined as needed)
        return False  # Placeholder for Dogecoin checks
    return False

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        wallet_address = request.form['wallet_address']
        blockchain = detect_blockchain(wallet_address)

        if blockchain == 'unknown':
            return render_template("index.html", error="Unknown address format. Please check your wallet address.")

        transactions = []
        exchanges_interacted = set()

        if blockchain == 'ethereum':
            transactions = get_ethereum_transactions(wallet_address)
        elif blockchain == 'bsc':
            transactions = get_bsc_transactions(wallet_address)
        elif blockchain == 'bitcoin':
            transactions = get_bitcoin_transactions(wallet_address)
        elif blockchain == 'solana':
            transactions = get_solana_transactions(wallet_address)
        elif blockchain == 'litecoin':
            transactions = get_litecoin_transactions(wallet_address)
        elif blockchain == 'dogecoin':
            transactions = get_dogecoin_transactions(wallet_address)
        
        if transactions:
            for tx in transactions:
                if is_transaction_to_exchange(tx, blockchain):
                    exchange_wallet = tx['to'] if blockchain in ['ethereum', 'bsc'] else 'Transaction to Exchange (Placeholder)' 
                    exchanges_interacted.add(exchange_wallet)

            return render_template("index.html", transactions=transactions, exchanges=exchanges_interacted, wallet_address=wallet_address, blockchain=blockchain)
        else:
            return render_template("index.html", error="No transactions found or an error occurred while fetching data.")

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
