from sortedcontainers import SortedDict
from collections import OrderedDict
import time
import heapq
MAX = 10 ** 8
MIN = 0
class StockTrading:
    def __init__(self):
        self.buy = SortedDict()
        # (type:0-market/1-limit, -buy_price, time) : (buy_volume, buyer_id)
        self.sell = SortedDict()
        # (type:0-market/1-limit, sell_price, time) : (sell_volume, seller_id)
        self.buy_stop = SortedDict()
        # (buy_price, time): (buy_volume, buyer_id)
        self.sell_stop = SortedDict()
        # (sell_price, time): (sell_volume, seller_id)
        self.min_buy = MAX
        self.max_sell = MIN

    def check_price(self, price):
        ans = []
        if self.buy_stop and price >= self.min_buy:
            buying = self.buy_stop.bisect((price, "99999999"))
            tobuy = []
            for i in range(buying):
                pt, vi = self.buy_stop.popitem(0)
                buy_price, buy_time = pt
                buy_volume, buyer_id = vi
                tobuy.append((buy_time, buy_price, buy_volume, buyer_id))
            tobuy.sort()
            for buy_time, buy_price, buy_volume, buyer_id in tobuy:
                ans.extend(self.trade(['market', 'buy', buyer_id, buy_volume, buy_price, buy_time]))
            if self.buy_stop:
                self.min_buy = self.buy_stop.peekitem(0)[0][0]
            else:
                self.min_buy = MAX
        if self.sell_stop and price <= self.max_sell:
            selling = len(self.sell_stop) - self.sell_stop.bisect((price, '0'))
            tosell = []
            for i in range(selling):
                pt, vi = self.sell_stop.popitem()
                sell_price, sell_time = pt
                sell_volume, seller_id = vi
                tosell.append((sell_time, sell_price, sell_volume, seller_id))
            tosell.sort()
            for sell_time, sell_price, sell_volume, seller_id in tosell:
                ans.extend(self.trade(['market', 'sell', seller_id, sell_volume, sell_price, sell_time]))
            if self.sell_stop:
                self.max_sell = self.sell_stop.peekitem()[0][0]
            else:
                self.max_sell = MIN
        return ans

    def trade(self, input):
        # [type: limit/market/stop, method:buy/sell, user_id, volume, price, order_time]
        # Market order - buy/sell:
        # Limit order - buy/sell:
        # Stop Order - automatic buy/sell, change the order type!:
        ans = []
        trade_type_txt, method, user_id, orig_volume, order_price, order_time = input
        trade_type = 0 if trade_type_txt == "market" else 1
        volume = orig_volume
        if trade_type_txt == "stop":
            if method == "buy":
                self.buy_stop[(order_price, order_time)] = (orig_volume, user_id)
                self.min_buy = min(order_price, self.min_buy)
            elif method == "sell":
                self.sell_stop[(order_price, order_time)] = (orig_volume, user_id)
                self.max_sell = max(order_price, self.max_sell)
            return ans
        other = []
        if method == "buy":
            while volume > 0 and self.sell and (trade_type == 0 or self.sell.peekitem(0)[0][0] == 0 or order_price >= self.sell.peekitem(0)[0][1]):  # If there are matched sell orders
                pt, vi = self.sell.popitem(0)
                sell_type, sell_price, sell_time = pt
                if sell_type == 0:
                    sell_price = order_price
                sell_volume, seller_id = vi
                sell_type_txt = "market" if sell_type == 0 else "limit"
                if volume >= sell_volume:
                    ans.append((sell_type_txt, "sell", seller_id, sell_price, sell_volume))
                    volume -= sell_volume
                else:
                    ans.append((sell_type_txt, "sell", seller_id, sell_price, volume))
                    sell_volume -= volume
                    volume = 0
                    self.sell[(sell_type, sell_price if sell_type == 1 else 0, sell_time)] = (sell_volume, seller_id)
                other.extend(self.check_price(sell_price))
            if volume > 0:  # If still unbought
                self.buy[(trade_type, - order_price if trade_type == 1 else 0, order_time)] = (volume, user_id)
            if volume < orig_volume:  # If bought some volume
                n = len(ans)
                sell_price, sell_volume = ans[0][3], 0
                for i in range(n):
                    curr_price = ans[i][3]
                    curr_volume = ans[i][4]
                    if curr_price == sell_price:
                        sell_volume += curr_volume
                    else:
                        ans.append((trade_type_txt, "buy", user_id, sell_price, sell_volume))
                        sell_price = curr_price
                        sell_volume = curr_volume
                ans.append((trade_type_txt, "buy", user_id, sell_price, sell_volume))
        elif method == "sell":
            while volume > 0 and self.buy and (trade_type == 0 or
                    self.buy.peekitem(0)[0][0] == 0 or order_price <= -self.buy.peekitem(0)[0][1]):  # If there are matched buy orders
                pt, vi = self.buy.popitem(0)
                buy_type, buy_price, buy_time = pt
                buy_price = - buy_price
                if buy_type == 0:
                    buy_price = order_price
                buy_volume, buyer_id = vi
                buy_type_txt = "market" if buy_type == 0 else "limit"
                if volume >= buy_volume:
                    ans.append((buy_type_txt, "buy", buyer_id, buy_price, buy_volume))
                    volume -= buy_volume
                else:
                    ans.append((buy_type_txt, "buy", buyer_id, buy_price, volume))
                    buy_volume -= volume
                    volume = 0
                    self.buy[(buy_type, - buy_price if buy_type == 1 else 0, buy_time)] = (buy_volume, buyer_id)
                other.extend(self.check_price(buy_price))
            if volume > 0:  # If still unsold
                self.sell[(trade_type, order_price if trade_type == 1 else 0, order_time)] = (volume, user_id)
            if volume < orig_volume:  # If sold some volume
                n = len(ans)
                buy_price, buy_volume = ans[0][3], 0
                for i in range(n):
                    curr_price = ans[i][3]
                    curr_volume = ans[i][4]
                    if curr_price == buy_price:
                        buy_volume += curr_volume
                    else:
                        ans.append((trade_type_txt, "sell", user_id, buy_price, buy_volume))
                        buy_price = curr_price
                        buy_volume = curr_volume
                ans.append((trade_type_txt, "sell", user_id, buy_price, buy_volume))

        return ans + other


    def cancel(self, input):
        # [type: limit / market / stop, method: buy / sell, user_id, volume, price, order_time]
        trade_type_txt, method, user_id, orig_volume, order_price, order_time = input
        ans = []
        vi = None
        if method == "buy":
            if trade_type_txt == "stop":
                if (order_price, order_time) in self.buy_stop:
                    vi = self.buy_stop.pop((order_price, order_time))
            trade_type = 1 if trade_type_txt == "limit" else 0
            if (trade_type, -order_price, order_time) in self.buy:
                vi = self.buy.pop((trade_type, -order_price, order_time))
        elif method == "sell":
            if trade_type_txt == "stop":
                if (order_price, order_time) in self.sell_stop:
                    vi = self.sell_stop.pop((order_price, order_time))
            trade_type = 1 if trade_type_txt == "limit" else 0
            if (trade_type, order_price, order_time) in self.sell:
                vi = self.sell.pop((trade_type, order_price, order_time))
        if vi:
            ans = [(trade_type_txt, method, user_id, order_price, orig_volume)]
        return ans

    def __str__(self):
        return f"Buy orders:{self.buy}\nSell orders:{self.sell}"


st = StockTrading()
out = st.trade(["limit", "buy", "user1", 5, 10, "20231106"])
print(out)
out = st.trade(["limit", "buy", "user2", 10, 9, "20231107"])
print(out)
out = st.trade(["limit", "sell", "user3", 4, 11, "20231108"])
print(out)
out = st.trade(["stop", "sell", "user2", 9, 8, "20231111"])
print(out)
out = st.trade(["limit", "sell", "user4", 6, 9, "20231109"])
print(out)
out = st.trade(["market", "sell", "user5", 15, 8, "20231110"])
print(out)
out = st.trade(["limit", "buy", "user2", 15, 8, "20231110"])
print(out)
print(st)
out = st.cancel(["limit", "sell", "user3", 4, 11, "20231108"])
print(out)
