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
            while volume > 0 and price >= self.sell[0][0]:
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

        elif input[0] == "sell":
            heapq.heappush(self.sell, (input[2], self.order_idx, input[1]))
        self.order_idx += 1

        # Compare and match!

