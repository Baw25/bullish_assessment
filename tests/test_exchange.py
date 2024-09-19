import unittest
import responses
from services.exchange import ExchangeAPI

# NOTE: Test cases for Exchange class.
class TestExchangeAPI(unittest.TestCase):
    def setUp(self):
        self.test_products = ['BTC-USD', 'ETH-USD']
        self.test_exchange = ExchangeAPI(self.test_products)

    @responses.activate
    def test_get_order_book_success(self):
        mock_response = {
            "bids": [["6247.58", "6.3578146", 2]],
            "asks": [["6251.52", "2", 1]],
        }
        
        responses.add(
            responses.GET,
            f'https://api.exchange.coinbase.com/products/BTC-USD/book?level=1',
            json=mock_response,
            status=200
        )

        order_book = self.test_exchange.get_order_book('BTC-USD')

        self.assertIsNotNone(order_book)
        self.assertEqual(order_book['product_id'], 'BTC-USD')
        self.assertEqual(order_book['bids'][0], '6247.58')
        self.assertEqual(order_book['asks'][0], '6251.52')

    @responses.activate
    def test_get_order_book_failure(self):
        # Ex) 404
        responses.add(
            responses.GET,
            f'https://api.exchange.coinbase.com/products/BTC-USD/book?level=1',
            json={"message": "Not Found"},
            status=404
        )

        order_book = self.test_exchange.get_order_book('BTC-USD')
        self.assertIsNone(order_book)

    @responses.activate
    def test_poll_all_success(self):
        mock_response_btc = {
            "bids": [["6247.58", "6.3578146", 2]],
            "asks": [["6251.52", "2", 1]],
        }
        mock_response_eth = {
            "bids": [["3247.58", "2.3578146", 1]],
            "asks": [["3251.52", "1.5", 1]],
        }

        responses.add(
            responses.GET,
            f'https://api.exchange.coinbase.com/products/BTC-USD/book?level=1',
            json=mock_response_btc,
            status=200
        )
        responses.add(
            responses.GET,
            f'https://api.exchange.coinbase.com/products/ETH-USD/book?level=1',
            json=mock_response_eth,
            status=200
        )

        result = self.test_exchange.poll_all()

        self.assertEqual(len(result), 2)
        self.assertIn('BTC-USD', result)
        self.assertIn('ETH-USD', result)
        self.assertEqual(result['BTC-USD']['bids'][0], '6247.58')
        self.assertEqual(result['ETH-USD']['bids'][0], '3247.58')

if __name__ == "__main__":
    unittest.main()
