import os
from datetime import datetime
from collections import defaultdict


def process_transaction(directory):
    # initialize the default values for the analysis
    daily_sales_volume = defaultdict(int)
    daily_sales_value = defaultdict(float)
    product_sales_volume = defaultdict(int)
    monthly_staff_sales = {}
    average_hourly_transaction_volume = {}

    for files in os.listdir(directory):

        # loop through the daily files to check for files that ends with .txt
        if files.endswith('.txt'):

            # join the directory path with the file name
            file_path = os.path.join(directory, files)
            file_date = files.split('.')[0]

            with open(file_path, 'r') as f:
                # loop through each lines in the .txt file
                for line in f:
                    # strip the line and split the line by comma
                    line = line.strip().split(',')

                    sales_staff_id, transaction_time, products_sold, sales_amount = line

                    # split the products_sold by '|' and strip the square brackets
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
                        # split the product by ':' to get the product and quantity sold
                        product_id, quantity = product.split(':')
                        quantity = int(quantity)

                        product_sales_volume[product_id] = product_sales_volume.get(product_id, 0) + quantity
                        quantity_sold += quantity

                    # update the daily sales volume and value
                    daily_sales_volume[transaction_date] += 1
                    daily_sales_value[transaction_date] += sales_amount

                    # update the monthly staff sales
                    if transaction_month not in monthly_staff_sales:
                        monthly_staff_sales[transaction_month] = {}
                    if sales_staff_id not in monthly_staff_sales[transaction_month]:
                        monthly_staff_sales[transaction_month][sales_staff_id] = 0
                    monthly_staff_sales[transaction_month][sales_staff_id] += sales_amount

                    # update the average hourly transaction volume
                    if transaction_hour not in average_hourly_transaction_volume:
                        average_hourly_transaction_volume[transaction_hour] = 0
                    average_hourly_transaction_volume[transaction_hour] += quantity_sold

    highest_sales_volume = max(daily_sales_volume, key=daily_sales_volume.get)
    highest_sales_value = max(daily_sales_value, key=daily_sales_value.get)
    most_sold_product = max(product_sales_volume, key=product_sales_volume.get)
    highest_sales_staff = {month: max(sales, key=sales.get) for month, sales in monthly_staff_sales.items()}
    highest_hourly_transaction_volume = max(average_hourly_transaction_volume, key=average_hourly_transaction_volume.get)
    
    print(f'Highest sales volume in a day: {highest_sales_volume} with transaction volume of {daily_sales_volume[highest_sales_volume]}')
    print(f'Highest sales value in a day: {highest_sales_value} with sales value of {daily_sales_value[highest_sales_value]}')
    print(f'Most sold product ID by volume: {most_sold_product}')
    print(f'Highest sales staff ID for each month: {highest_sales_staff}')
    print(f'Highest hour of the day by average transaction volume: {highest_hourly_transaction_volume}')

# process_transaction(directory)











































