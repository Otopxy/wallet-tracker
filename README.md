# wallet-tracker
Cryptocurrency Wallet Tracker

This project is a cryptocurrency wallet tracker built using Python, Flask, and various public APIs. The application allows users to track the activity of a cryptocurrency wallet address, filter transactions from the past 7 days, and identify interactions with known centralized exchanges like Binance, Coinbase, and others.

Features

Blockchain Detection: Automatically detects the blockchain of a wallet address (Ethereum, Binance Smart Chain, Bitcoin, Solana, Litecoin, Dogecoin).
Transaction History: Fetches transaction history from multiple blockchains and displays it on the web interface.
Last 7 Days Filter: Only displays transactions that occurred in the past 7 days.
Exchange Detection: Identifies if a wallet address has interacted with known centralized exchanges.
Supported Blockchains

Ethereum (ETH)
Binance Smart Chain (BSC)
Bitcoin (BTC)
Solana (SOL)
Litecoin (LTC)
Dogecoin (DOGE)
Setup

Prerequisites
Make sure you have Python 3.6 or higher installed. You’ll also need a text editor like VS Code or Sublime Text.

Clone the Repository

cd cryptocurrency-wallet-tracker

Create a Virtual Environment (optional, but recommended):

`python -m venv venv`

Activate the Virtual Environment:

On Windows:

venv\Scripts\activate

On macOS/Linux:

source venv/bin/activate

Install Dependencies:
Install the required Python libraries using pip:

pip install -r requirements.txt

Set Up API Keys:
You need to obtain API keys for Ethereum (Etherscan), Binance Smart Chain (BSCScan), and other relevant APIs.

* Etherscan API
* BSCScan API
* Solana API
* Blockchair API
  
Once you have the keys, replace the placeholders in the app.py file:

* ETHERSCAN_API_KEY = 'YourEtherscanAPIKey'
* BSCSCAN_API_KEY = 'YourBSCScanAPIKey'
* BLOCKCHAIR_API_KEY = 'YourBlockchairAPIKey'

Run the Application:
`python app.py`
This will start a local development server.
Access the Application:
Open your web browser and go to:

http://127.0.0.1:5000/
Requirements
Python 3.6 or higher
Flask
Requests
API keys for Ethereum, BSC, Solana, Litecoin, Dogecoin, etc.
Install Dependencies
You can install all necessary dependencies using:

pip install -r requirements.txt
Usage

Once the app is running, navigate to the URL http://127.0.0.1:5000/ in your browser.

Enter a wallet address in the input box.

You can input any valid cryptocurrency wallet address (Ethereum, Binance Smart Chain, Bitcoin, etc.).

View transaction history: The app will display the most recent transactions for the provided wallet address within the past 7 days.

Exchange Detection: If the wallet has interacted with any known centralized exchanges, the app will highlight these interactions.

Blockchain Information: The app automatically detects the blockchain based on the wallet address format.



Troubleshooting

Error: "No transactions found":
This may happen if the provided wallet address has no recent transactions or the address is invalid.

Error: "Unknown address format":
Make sure the wallet address is in the correct format. The app detects Ethereum, BSC, Bitcoin, Solana, Litecoin, and Dogecoin addresses. If you're using another blockchain, it may not be supported yet.

API Rate Limits:
Most public APIs have rate limits. If you exceed the allowed number of requests, you might receive an error. Try waiting a few minutes before retrying or check the API documentation for rate limits.
Contributing

Feel free to contribute to the project by opening issues or submitting pull requests. If you have any ideas for new features or improvements, feel free to reach out.

To Contribute:
Fork the repository.

Create a new branch (git checkout -b feature/your-feature-name).

Make your changes and commit them (git commit -am 'Add feature').

Push to the branch (git push origin feature/your-feature-name).

Open a pull request with a description of your changes.

License

This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgements

Etherscan API for Ethereum transaction data.

BSCScan API for Binance Smart Chain transaction data.

Solana API for Solana transaction data.

Blockchair API for Bitcoin, Litecoin, and Dogecoin data.

Additional Notes:
You can expand this project by adding support for more blockchains.

The app can be deployed to platforms like Heroku, AWS, or DigitalOcean for production use.
