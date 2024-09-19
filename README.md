# L1 Order Book Data Storage

## Author 
Blake Wills

## Overview
This project fetches Level 1 (L1) order book data from an exchange API (Coinbase API in this case) for multiple product pairs and stores it in a Redis database. 
The order book data consists of the best bid and ask prices and their respective volumes.

## Features
- Fetch real-time order book data from Coinbase for multiple products (currencies).
- Store order book data in Redis (using the primary key (`orderbook:<product_id>`)).
- Unit tests with testcontainers and assertions to check functionality.

## Dependencies
- Docker (running locally)
- Redis (running locally with port 6379)
- All python packages defined within requirements.txt
- Coinbase Exchange API (https://docs.cdp.coinbase.com/exchange/reference/exchangerestapi_getproductbook/)

## Setup Directions
1. Create a virtual environment and install dependencies in requirements.txt:
   For example:
    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

2. Run the get L1 order book data script to fetch and store data:
   For example, run the command with an input csv containing various product IDs:
    ```bash
    python get_L1_orderbook_data.py --csv example_products.csv
    ```

3. Run the query Redis data script to query some of the data:
   For example, query by product ID:
    ```bash
    python query_redis_data.py --product_id BTC-USD
    ```    

4. Run all unit tests for the exchange class and db store class:
    ```bash
    python -m unittest
    ```

## Redis Data Schema
- **Key Format**: `orderbook:<product_id>:<timestamp>`
- **Fields**:
  - `bids`: Best bid price and volume (JSON format)
  - `asks`: Best ask price and volume (JSON format)
  - `timestamp`: Timestamp of the order book snapshot
  - `sequence`: book sequence

## Python classes 
The python classes for the script can be found in the servies folder:
- RedisStore
- ExchangeAPI

Other potential classes if there was more time could have been child classes for the various exchanges with the parent 
ExchangeAPI and other various ORM or access pattern classes to the stored data.


## Project Management Steps and Process

The following were steps taken for this project could have been broken down into Agile stories/tasks:

1. Set Up Development Environment For Project (single story with 3 tasks)
- Create a virtual environment for Python to manage dependencies.
- Install necessary libraries (requests, redis, testcontainers, etc.)
- Set up Redis for local development or via Docker if necessary

2. Investigate and identify the exchange endpoints for fetching L1 book data (ex: Coinbase API).
- Identify candidate exchanges and compare and contrast
- Investigate Swagger API document and/or other relevant document information 

3. Implement Python classes for Redis querying and storage and for the Exchange 
- Write a Python class to connect to the exchange
- Ensure that the data includes bids, asks, and timestamps
- Handle potential errors or exceptions, such as network issues or API rate limits

4. Design a key structure in Redis to store the L1 order book data (e.g., orderbook:<product_id>:<timestamp>).
- Ensure that data is stored in a searchable format
- Add methods to list and retrieve data from Redis

5. Write unit tests using unittest and testcontainers.
- Test storing and retrieving L1 order book data in Redis
- Test the exchange API class 

6. Create a script that polls the Exchange API and stores the data and another script to query the data.
- get_L1_orderbook_data script
- query_redis_data script

7. Write a README file to document the project.

## Future Project Management Directions Not Covered 

A. Implement retries with exponential backoff if the Exchange API responds with rate limit errors.
Add optimizations to reduce the number of API calls.

B. Add support for fetching L1 order book data from other crypto exchanges (ex: Binance, Kraken) to diversify data sources.

C. Improve Redis storage and retrieval methods to support more complex queries (ex: retrieve data for a specific time range).

D. Package the project for deployment to cloud platforms like AWS or GCP.
