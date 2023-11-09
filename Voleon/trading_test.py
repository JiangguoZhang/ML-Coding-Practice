from sortedcontainers import SortedDict


class Stock:
    def __init__(self):
        self.buy = SortedDict() # {(-price, datatime): (volume, user_info, order_type)}
        self.sell = SortedDict() # {(price, datatime): (volume, user_info, order_type)}

    def trade(self, order_type, trade_type, user_info, datetime, price, volume):
        dynamic_volume = volume
        ans = [] # (order_type, trade_type, user_info, date_time, price, volume, other_user, other_date_time)
        if trade_type == "buy":
            while dynamic_volume > 0 and self.sell and self.sell.peekitem(0)[0][0] <= price:
                sell_key, sell_value = self.sell.popitem(0)
                sell_price, sell_time = sell_key
                sell_volume, seller_info, sell_order_type = sell_value
                if dynamic_volume >= sell_volume:
                    dynamic_volume -= sell_volume
                    ans.append((sell_order_type, "sell", seller_info, sell_time, sell_price, sell_volume, user_info, datetime))
                else:
                    ans.append((sell_order_type, "sell", seller_info, sell_time, sell_price, dynamic_volume, user_info, datetime))
                    self.sell[(sell_price, sell_time)] = (sell_volume - dynamic_volume, seller_info, sell_order_type)
                    dynamic_volume = 0
            if dynamic_volume > 0:
                self.buy[(-price, datetime)] = (dynamic_volume, user_info, order_type)
        elif trade_type == "sell":
            while dynamic_volume > 0 and self.buy and -self.buy.peekitem(0)[0][0] >= price:
                buy_key, buy_value = self.buy.popitem(0)
                buy_price, buy_time = buy_key
                buy_volume, buyer_info, buy_order_type = buy_value
                buy_price = - buy_price
                if dynamic_volume >= buy_volume:
                    dynamic_volume -= buy_volume
                    ans.append((buy_order_type, "buy", buyer_info, buy_time, buy_price, buy_volume, user_info, datetime))
                else:
                    ans.append((buy_order_type, "buy", buyer_info, buy_time, buy_price, dynamic_volume, user_info, datetime))
                    self.buy[(-buy_price, buy_time)] = (buy_volume - dynamic_volume, buyer_info, buy_order_type)
                    dynamic_volume = 0
            if dynamic_volume > 0:
                self.sell[(price, datetime)] = (dynamic_volume, user_info, order_type)
        return ans

st = Stock()
out = st.trade("limit", "buy", "user1", "20231106", 10, 5)
print(out)
out = st.trade("limit", "buy", "user2", "20231107", 9, 10)
print(out)
out = st.trade("limit", "sell", "user3", "20231108", 11, 4)
print(out)
# out = st.trade(["stop", "sell", "user2", 9, 8, "20231111"])
# print(out)
out = st.trade("limit", "sell", "user4", "20231109", 9, 6)
print(out)
# out = st.trade("market", "sell", "user5", "20231110", 8, 15)
# print(out)
# out = st.trade("limit", "buy", "user2", "20231110", 8, 15)
# print(out)
# print(st)
# out = st.cancel(["limit", "sell", "user3", 4, 11, "20231108"])
# print(out)