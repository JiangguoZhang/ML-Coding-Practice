from collections import OrderedDict
import time
import heapq
class StockTrading:
    def __init__(self):
        self.buy = []
        self.sell = []
        self.order_idx = 0

    def trade(self, input):
        # [limit/market/stop buy/sell volume price]
        # Market order:
        # Limit order:
        # Stop Order:
        # Case 1:
        ans = []
        orig_volume, price = input[1], input[2]
        volume = orig_volume
        if input[0] == "buy":
            while volume > 0 and self.sell and price >= self.sell[0][0]:
                sell_price, sell_id, sell_volume = heapq.heappop(self.sell)
                if volume >= sell_volume:
                    volume -= sell_volume
                    ans.append(('sell', sell_volume, sell_price))
                else:
                    ans.append(('sell', volume, sell_price))
                    sell_volume -= volume
                    volume = 0
                    heapq.heappush(self.sell, (sell_price, sell_id, sell_volume))
            if volume > 0:
                heapq.heappush(self.buy, (-price, self.order_idx, volume))
                self.order_idx += 1
            if volume < orig_volume:
                n = len(ans)
                sold_price, sold_volume = ans[0][2], 0
                for i in range(n):
                    if ans[i][2] == sold_price:
                        sold_volume += ans[i][1]
                    else:
                        ans.append(("buy", sold_volume, sold_price))
                        sold_price = ans[i][2]
                        sold_volume = ans[i][1]
                ans.append(("buy", sold_volume, sold_price))

        elif input[0] == "sell":
            while volume > 0 and self.buy and price <= -self.buy[0][0]:
                buy_price, buy_id, buy_volume = heapq.heappop(self.buy)
                buy_price = - buy_price
                if volume >= buy_volume:
                    volume -= buy_volume
                    ans.append(('buy', buy_volume, buy_price))
                else:
                    ans.append(("buy", volume, buy_price))
                    buy_volume -= volume
                    volume = 0
                    heapq.heappush(self.buy, (- buy_price, buy_id, buy_volume))
            if volume > 0:
                heapq.heappush(self.sell, (price, self.order_idx, volume))
                self.order_idx += 1
            if volume < orig_volume:
                n = len(ans)
                buy_price, buy_volume = ans[0][2], 0
                for i in range(n):
                    if ans[i][2] == buy_price:
                        buy_volume += ans[i][1]
                    else:
                        ans.append(("sell", buy_volume, buy_price))
                        buy_price = ans[i][2]
                        buy_volume = ans[i][1]
                ans.append(("sell", buy_volume, buy_price))

        return ans


st = StockTrading()
out = st.trade(['buy', 5, 10])
print(out)
out = st.trade(['buy', 10, 9])
print(out)
out = st.trade(['sell', 4, 11])
print(out)
out = st.trade(['sell', 6, 9])
print(out)
