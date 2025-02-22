"""
Monieshop is a supermarket that sells different products to its customers. It uses a digital accounting system to track its sales transactions.
The digital accounting system uses text files to store transaction data. Here is a brief description of the file format:

Each text file contains the transaction data for 1 day.
A single line in a transaction file stores information related to 1 transaction in a comma-separated format. The information present is: 
salesStaffId
transaction time
The products sold. (format “[productId1:quantity|productId2:quantity]”)
sale amount

Example for a line in a transaction file: “4,2025-01-01T16:58:53,[726107:5|553776:5],2114.235”
You’re asked to write analytics software that reads through 2024 transactions’ files and reports the following metrics:
Highest sales volume in a day
Highest sales value in a day
Most sold product ID by volume
Highest sales staff ID for each month.
Highest hour of the day by average transaction volume

"""
import os
from datetime import datetime
from collections import defaultdict

directory = '/home/uthman/coding/DreamDevs-Hackathon/mp-hackathon-sample-data/test-case-2'

def process_transaction(directory):
    # initialize the default values for the analysis
    daily_sales_volume = defaultdict(int)
    daily_sales_value = defaultdict(float)
    product_sales_volume = defaultdict(int)
    monthly_staff_sales = {}

    for files in os.listdir(directory):

        # loop through the daily files to check for files that ends with .txt

        if files.endswith('.txt'):

            file_path = os.path.join(directory, files)
            file_date = files.split('.')[0]

            with open(file_path, 'r') as f:
                # loop through each lines in the .txt file
                for line in f:
                    line = line.strip().split(',')
                    sales_staff_id, transaction_time, products_sold, sales_amount = line
                    products_sold = products_sold.strip('[]').split('|')
                    
                    sales_amount = float(sales_amount)

                    # Parse the transaction_time to convert the time to datetime object
                    try:
                        transaction_datetime = datetime.strptime(transaction_time, '%Y-%m-%dT%H:%M:%S')
                    except ValueError:
                        transaction_datetime = datetime.strptime(transaction_time, '%Y-%m-%dT%H:%M')
                
                    transaction_date = transaction_datetime.date()
                    transaction_hour = transaction_datetime.hour
                    transaction_month = transaction_datetime.strftime('%Y-%m')
                
                    quantity_sold = 0
                    for product in products_sold:
                        product_id, quantity = product.split(':')
                        quantity = int(quantity)

                        product_sales_volume[product_id] = product_sales_volume.get(product_id, 0) + quantity
                        quantity_sold += quantity

                    # update the daily sales volume and value
                    daily_sales_volume[transaction_date] += 1
                    daily_sales_value[transaction_date] += sales_amount

                    

    highest_sales_volume = max(daily_sales_volume, key=daily_sales_volume.get)
    highest_sales_value = max(daily_sales_value, key=daily_sales_value.get)
    most_sold_product = max(product_sales_volume, key=product_sales_volume.get)
    
    print(f'Highest sales volume in a day: {highest_sales_volume}')
    print(f'Highest sales value in a day: {highest_sales_value}')
    print(f'Most sold product ID by volume: {most_sold_product}')

process_transaction(directory)











































