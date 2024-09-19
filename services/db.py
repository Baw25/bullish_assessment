import requests
import redis
import json
import time
from datetime import datetime

#NOTE: Wrapper class to query Redis to pull the book data for a given product id. If there was more time
# we would include more queries for auction and sequence data if we decide to pull more L2 and L3 like data.
class RedisStore:
    def __init__(self, host='localhost', port=6379, db=0):
        self.client = redis.StrictRedis(host=host, port=port, db=db)

    def store_order_book(self, data):
        for product_id, order_data in data.items():
            timestamp = order_data['timestamp']
            
            orderbook_entry = json.dumps({
                'sequence': order_data.get('sequence', ""),
                'bids': order_data['bids'],
                'asks': order_data['asks'],
                'timestamp': timestamp,
            })

            unix_timestamp = time.mktime(time.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f"))
            # NOTE: Use product_id primarily for index key, but could have used timestamp too
            index_key = f"orderbook:index:{product_id}"
            self.client.zadd(index_key, {orderbook_entry: unix_timestamp})            

    def get_order_book(self, product_id):
        index_key = f"orderbook:index:{product_id}"

        results = self.client.zrevrange(index_key, 0, 0)
        if not results:
            return None

        order_book = json.loads(results[0].decode())

        return order_book        

    def get_latest_order_book(self, product_id):
        index_key = f"orderbook:index:{product_id}"
        latest_timestamp = self.client.zrange(index_key, -1, -1)[0].decode()
        key = f"orderbook:{product_id}:{latest_timestamp}"

        return self.client.hgetall(key)

    def get_order_book_in_range(self, product_id, start_time, end_time): 
        index_key = f"orderbook:index:{product_id}"
        start = time.mktime(time.strptime(start_time, "%Y-%m-%dT%H:%M:%S.%f"))
        end = time.mktime(time.strptime(end_time, "%Y-%m-%dT%H:%M:%S.%f"))        
        results = self.client.zrangebyscore(index_key, start, end)

        print("Raw results from Redis:", results)
        order_books = [json.loads(result.decode()) for result in results]

        return order_books

    def get_order_book_sequence(self, product_id):
        # TODO: Get the product books sequence from L2 or L3 data
        pass

    def get_order_book_auction(self, product_id):
        # TODO: Get the product books auction object from L2 or L3 data
        pass        

    def list_keys(self):
        return self.client.keys('orderbook:*')
