# Script for quering Redis database for the L1 order book data

from services.db import RedisStore
import json
import argparse
import logging

# Logger config
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Query the Redis DB and pull all stored data.")
    
    # Query by product id optionally
    parser.add_argument(
        '--product_id',
        type=str,
        help="Filter the data by specific product ID (ex: BTC-USD)"
    )

    parser.add_argument(
        '--start_time',
        type=str,
        help="Start timestamp (ex: '2021-02-12T01:09:23.000000Z').",
        required=False
    )

    parser.add_argument(
        '--end_time',
        type=str,
        help="End timestamp (ex: '2021-02-12T01:10:00.000000Z').",
        required=False
    )

    input_args = parser.parse_args()
    redis_store = RedisStore()

    if input_args.product_id:
        # If a timestamp range is provided:
        if input_args.start_time and input_args.end_time:
            order_data = redis_store.get_order_book_in_range(input_args.product_id, input_args.start_time, input_args.end_time)
            if order_data:
                for book in order_data:
                    bids = book['bids']
                    asks = book['asks']                   
                    logger.info(f"Product ID: {input_args.product_id}")
                    logger.info(f"Timestamp: {book['timestamp']}")
                    logger.info(f"Bids: price ${bids[0]}, volume: {bids[1]}, count: {bids[2]}")
                    logger.info(f"Asks: price ${asks[0]}, volume: {bids[1]}, count: {bids[2]}")
                    logger.info(f"Sequence: {book['sequence']}")
            else:
                logger.warning(f"No data found for product ID: {input_args.product_id} and range: {input_args.start_time} to {input_args.end_time}")
        else:
            order_data = redis_store.get_order_book(input_args.product_id)
            if order_data:
                bids = order_data['bids']
                asks = order_data['asks']
                logger.info(f"Product ID: {input_args.product_id}")
                logger.info(f"Bids: price ${bids[0]}, volume: {bids[1]}, count: {bids[2]}")
                logger.info(f"Asks: price ${asks[0]}, volume: {bids[1]}, count: {bids[2]}")
                logger.info(f"Timestamp: {order_data['timestamp']}")
            else:
                logger.warning(f"No data found for product ID: {input_args.product_id}")
    else:
        logger.warning("Please specify a product ID to query the order book.")    

if __name__ == "__main__":
    main()
