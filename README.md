# Crypto-Bot
This is simple crypto bot with implemented communication. The communication in this case is simple publisher/subscriber pattern using paho-mqtt and sending signals to email. 
As for the strategy of the crypto bot that is implemented here, it is using RSI(Relative Strength Index) and two Moving Averages to know when to buy and when to sell the crypto. 
The signals for buying and selling the crypto are as follows: 
1. If the shorter moving average crosses the longer moving average in the upward direction and RSI is below 30(meaning that the market is oversold) that is when the buy signal is happening
1. If the shorter moving average crosses the longer moving average in the downward direction and RSI is above 70(meaning that the market is overbought) that is when the sell signal is happening

## Use of this crypto bot
The use of this crypto bot is to represent communication as well as the strategy in this case. 
There are two types of communication implemented inside:
1. Sending buy and sell signals of the current price that the crypto is bought on your email account that you provide
1. Sending buy and sell signals using MQTT publisher/subscriber pattern

## References
1. https://python-binance.readthedocs.io/en/latest/
1. https://mrjbq7.github.io/ta-lib/doc_index.html
1. https://docs.python.org/3/library/smtplib.html

**Disclaimer - This is in no case financial advice and I can't control what happens with your money when using this crypto-bot. Use this crypto-bot on your own risk.**
