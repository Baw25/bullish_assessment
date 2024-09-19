# NOTE: Collection of utility functions found here
import csv

def read_product_ids_from_csv(file_path):
    product_ids = []

    try:
        with open(file_path, mode='r') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                if row:  
                    product_ids.append(row[0])
    except FileNotFoundError:
        print(f"Error: File {file_path} not found!")

    return product_ids