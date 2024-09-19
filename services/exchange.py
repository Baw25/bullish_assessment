import requests
import json
from datetime import datetime

# NOTE: Idea here is to create API wrapper for a given exchange url and path to pull L1 data.
# If there was more time, we would expand this to be an abstract Exchange class to incorporate 
# multiple exchange L1 book data.
# SEE COINBASE SOURCE: https://docs.cdp.coinbase.com/exchange/reference/exchangerestapi_getproductbook
class ExchangeAPI:
    DEFAULT_BASE_URL = 'https://api.exchange.coinbase.com'

    def __init__(self, products, base_url = '', url_path = '/products'):
        self.products = products
        self.base_url = base_url or self.DEFAULT_BASE_URL
        self.url_path = url_path

    def get_order_book(self, product_id, level=1):
        try:
            response = requests.get(f'{self.base_url}{self.url_path}/{product_id}/book', params={'level': level})
            response.raise_for_status()
            data = response.json()

            # NOTE: Mainly structured for L1 only for the sake of time
            return {
                'product_id': product_id,
                'bids': data['bids'][0],
                'asks': data['asks'][0],
                'timestamp': datetime.utcnow().isoformat()
            }
        except requests.exceptions.RequestException as err:
            print(f"Error fetching data from exchange for {product_id}: {err}")
            return None

    def get_product_stats(self, product_id):
        # TODO: Implement product stats for further L1 data 
        pass 

    def get_all_product_volume(self, product_id):
        # TODO: Implement all product volume for to pull all volume data about product
        pass 

    def poll_all(self):
        result = {}
        for product_id in self.products:
            data = self.get_order_book(product_id)
            if data:
                result[product_id] = data

        return result

