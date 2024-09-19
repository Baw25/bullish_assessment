import unittest
import json
import time
from datetime import datetime
from testcontainers.redis import RedisContainer
from services.db import RedisStore

# NOTE: Test cases for Redis query class where a Redis 
# test container is used as instructed in the prompt.
class TestRedisStore(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # NOTE: Set up the Redis test container
        cls.redis_container = RedisContainer().start()
        cls.redis_host = cls.redis_container.get_container_host_ip()
        cls.redis_port = cls.redis_container.get_exposed_port(6379)
        cls.redis_store = RedisStore(host=cls.redis_host, port=cls.redis_port)

    @classmethod
    def tearDownClass(cls):
        cls.redis_container.stop()

    def setUp(self):
        self.seed_order_data = {
            'BTC-USD': {
                'sequence': '12345',
                'bids': [['6247.58', '6.3578146', 2]],
                'asks': [['6251.52', '2', 1]],
                'timestamp': '2024-09-19T12:00:00.000000'
            },
            'ETH-USD': {
                'sequence': '54321',
                'bids': [['3247.58', '2.3578146', 1]],
                'asks': [['3251.52', '1.5', 1]],
                'timestamp': '2024-09-19T12:05:00.000000'
            }
        }

    def test_store_and_retrieve_order_book(self):
        self.redis_store.store_order_book(self.seed_order_data)
        order_book = self.redis_store.get_order_book('BTC-USD')

        self.assertIsNotNone(order_book)
        self.assertEqual(order_book['sequence'], '12345')
        self.assertEqual(order_book['bids'][0][0], '6247.58')
        self.assertEqual(order_book['asks'][0][0], '6251.52')

    def test_get_order_book_in_range(self):
        self.redis_store.store_order_book(self.seed_order_data)
        start_time = '2024-09-19T11:59:00.000000'
        end_time = '2024-09-19T12:06:00.000000'
        order_books = self.redis_store.get_order_book_in_range('BTC-USD', start_time, end_time)

        self.assertEqual(len(order_books), 1)
        self.assertEqual(order_books[0]['sequence'], '12345')

    def test_get_order_book_with_no_results_in_range(self):
        self.redis_store.store_order_book(self.seed_order_data)
        start_time = '2024-09-19T10:00:00.000000'
        end_time = '2024-09-19T11:00:00.000000'
        order_books = self.redis_store.get_order_book_in_range('BTC-USD', start_time, end_time)

        self.assertEqual(len(order_books), 0)

    def test_list_keys(self):
        self.redis_store.store_order_book(self.seed_order_data)

        keys = self.redis_store.list_keys()

        self.assertTrue(any(b'orderbook:index:BTC-USD' in key for key in keys))
        self.assertTrue(any(b'orderbook:index:ETH-USD' in key for key in keys))

    def test_store_and_retrieve_multiple_order_books(self):
        self.redis_store.store_order_book(self.seed_order_data)

        order_book = self.redis_store.get_order_book('ETH-USD')

        self.assertIsNotNone(order_book)
        self.assertEqual(order_book['sequence'], '54321')
        self.assertEqual(order_book['bids'][0][0], '3247.58')
        self.assertEqual(order_book['asks'][0][0], '3251.52')

if __name__ == "__main__":
    unittest.main()

