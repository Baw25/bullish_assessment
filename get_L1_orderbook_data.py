# Script for getting the remote L1 order book data

import argparse
import logging
from services.db import RedisStore
from services.exchange import ExchangeAPI
from services.utility import read_product_ids_from_csv

# Logger config
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def main(): 
    parser = argparse.ArgumentParser(description="Fetch L1 order book data from a crypto exchange.")

    parser.add_argument(
        '--csv',
        type=str,
        help="Path to CSV file containing product IDs"
    )

    parser.add_argument(
        '--product_ids',
        nargs='+',
        help="List of product IDs to fetch from the exchange (ex: BTC-USD ETH-USD)"
    )    

    input_args = parser.parse_args()

    #NOTE: Use the product ids from the csv if provided 
    product_ids = []
    if input_args.csv:
        product_ids = read_product_ids_from_csv(input_args.csv)
        if not product_ids:
            logger.error("No valid product IDs found in csv file!")

            return 

    if input_args.product_ids:
        product_ids.extend(input_args.product_ids)

    if not product_ids:
        logger.error("No product IDs provided!")
        
        return

    #NOTE: Fetch and store L1 data in Redis
    logger.info(f"Fetching order book data for product IDs: {product_ids}")
    exchange = ExchangeAPI(product_ids)
    orderbook_data = exchange.poll_all()

    redis_store = RedisStore()
    redis_store.store_order_book(orderbook_data)

    logger.info("Successfully stored order book data.")
    logger.debug(f"Stored keys in Redis: {redis_store.list_keys()}")               

if __name__ == "__main__":
    main()