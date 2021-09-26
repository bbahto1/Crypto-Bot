from binance.enums import ORDER_TYPE_MARKET, SIDE_BUY
import numpy as np
from binance.client import Client
import config
import talib
import smtplib
from datetime import datetime
from communication import publisher
from binance.enums import *

password_for_email_account = "your_email_password"
email_address = 'your_email_address@gmail.com'

# for buying and selling the real crypto you need to enter your own crypto that you want to trade and amount
# depending on your account balance and how much you want to invest 
TRADE_SYMBOL = 'BTCUSDT'
TRADE_QUANTITY = 0.001

# limits for oversold and overbought market RSI 
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30

# defining range for moving average and RSI period
# you can change this depending on your trading strategy
SHORT_MA_RANGE = 12
LONG_MA_RANGE = 25
RSI_PERIOD = 10

class CryptoBot:
    def __init__(self, api_key, api_secret):
        self.client = Client(api_key, api_secret)
    
    def EMA(self, interval, price):
        return talib.EMA(price, timeperiod = interval)
    
    def SMA(self, interval, price):
        return talib.SMA(price, timeperiod = interval)
    
    def my_RSI(self, interval, price):
        return talib.RSI(price, timeperiod = interval)
    
    def send_email(self, message_signal):
        global password_for_email_account, email_address
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(email_address, password_for_email_account)
        subject = "Message from crypto-bot"
        body = message_signal
        email_send = f'subject: {subject}\n\n{body}'

        server.sendmail(
            "sender_email_address@gmail.com", 
            "reciever_email_address@gmail.com", 
            email_send
        )

        print("Email is sent")
        server.quit()

    def place_order(self, symbol, side, type, value):
        if side == Client.SIDE_BUY:
            order = self.client.create_order(
                symbol=symbol,
                side=side,
                type=type,
                quoteOrderQty=value)
        else: 
            order = self.client.create_order(
                symbol=symbol,
                side=side,
                type=type,
                quantity=value)
        print("Order made:\n{}".format(order))
    
    def get_trades(self, type_of_comm = 3):
        is_traded = False
        while True:
            kline = self.client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1MINUTE, "30 min ago UTC")
            closing_price = np.zeros(len(kline))
            for i in range(0, len(kline)):
                closing_price[i] = float(kline[i][4])
            
            Short_EMA_of_closing_price = self.EMA(SHORT_MA_RANGE, closing_price)
            Long_EMA_of_closing_price = self.EMA(LONG_MA_RANGE, closing_price)
            RSI_user = self.my_RSI(RSI_PERIOD, closing_price)
            messages_to_be_sent = []
            if Short_EMA_of_closing_price[-1] >= Long_EMA_of_closing_price[-1] and RSI_user[-1] < RSI_OVERSOLD:
                if is_traded:
                    print("Nothing to do, we alredy own this stock. It is oversold !")
                else:
                    print("Buy signal")
                    if type_of_comm == 1:
                        self.send_email("Bought the crypto at price: %f, at the time: %s" %(closing_price[i], str(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))))
                    else:
                        messages_to_be_sent.append("Bought the crypto at price: %f, at the time: %s" %(closing_price[i], str(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))))
                        # I advise you visit binance documentation on this matter
                        # so that you can create your own order
                        # place_order() is user defined function
                        # Keep in mind when placing an order that this is buy side
                        # https://binance-docs.github.io/apidocs/spot/en/#new-order-trade
                        # https://python-binance.readthedocs.io/en/latest/binance.html#binance.client.Client.create_order
                        """ 
                        order_succeded = self.place_order(symbol, side, type, value)
                        """
                        order_succeded = True
                    if order_succeded:
                        is_traded = True
            if Short_EMA_of_closing_price[-1] <= Long_EMA_of_closing_price[-1] and RSI_user[-1] > RSI_OVERBOUGHT:
                if is_traded:
                    print("Sell signal")
                    if type_of_comm == 1:
                        self.send_email("Sold the crypto at price: %f, at the time: %s" %(closing_price[i], str(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))))
                    else:
                        messages_to_be_sent.append("Sold the crypto at price: %f, at the time: %s" %(closing_price[i], str(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))))
                        # I advise you visit binance documentation on this matter
                        # so that you can create your own order
                        # place_order() is user defined function
                        # Keep in mind when placing an order that this is sell side
                        # https://binance-docs.github.io/apidocs/spot/en/#new-order-trade
                        # https://python-binance.readthedocs.io/en/latest/binance.html#binance.client.Client.create_order
                        """ 
                        order_succeded = self.place_order(symbol, side, type, value)
                        """
                    order_succeded = True
                    if order_succeded:
                        is_traded = False
                else:
                    print("Overbought, don't buy any. Nothing to do !")
            if type_of_comm == 2:
                publisher.run(messages_to_be_sent)


if __name__ == '__main__':
    crm = CryptoBot(config.API_KEY, config.SECRET_KEY)
    # type of communication:
    # 1 - send email
    # 2 - pub/sub
    # 3 - don't want any communication
    crm.get_trades(3)

    

    