# Binance Portfolio Tracker

Welcome to Binance Portfolio Tracker. This project help you to track your portfolio more efficiently.


## Advantages over Binance dashboard:

- Average cost of each coin
- Current profit based on dollar and percentage
- Future profit and balance based on your target price
- Total profit
- Future total profit

## Usage

1- Install libraries with `pip install -r requirements.txt` command.

2- Binance -> Profile -> API Management

3- Create an API

4- Copy the API key and paste it into the corresponding API_KEY section in the API KEYS.json file located in the project folder.

5- Do the same for the Secret Key as for the API Key.

Note: Keep your Secret Key because the Secret Key cannot be viewed again.

6- Run `UpdatePortfolio.py` file. It will gather the information from your account and write it down to `Portfolio.xlsx`


### Some known bugs:

1- To calculate the Average Cost, the total amount invested in each coin must be known. The Python file will try to extract this information from the trades you made. But it can make mistakes because it tries to extract this information only from your buys and sells. If you convert a coin, send it to another account, or buy another coin with that coin, the total deposited amount will be incorrectly calculated as there is no selling transaction. To fix this, it is recommended to manually correct the errors in the Total Purchased column, if you know how many dollars you have invested in each coin.

2- If you are using excel in a language other than Turkish, please change the formula in cells L2 and L5 according to your excel language.

