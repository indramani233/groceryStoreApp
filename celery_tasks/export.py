from celery import Celery, shared_task
import csv
from models.product import Product
from flask import current_app, flash

celery = Celery()

@shared_task
def export_product_details():
    # Fetch product details
    products = Product.query.all()

    # Define CSV columns and rows
    csv_columns = ['Name', 'Stock Remaining', 'Description', 'Price', 'Units Sold']
    rows = []

    # Populate CSV rows with product details
    for product in products:
        row = {
            'Name': product.title,
            'Stock Remaining': product.quantity_available,
            'Description': product.description,
            'Price': product.cost,
            #'Units Sold': product.units_sold
        }
        rows.append(row)

    # Path to save the CSV file (modify the path as needed)
    file_path = current_app.config['EXPORT_PATH'] + 'product_details.csv'

    # Write product details to a CSV file
    with open(file_path, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
        writer.writeheader()
        writer.writerows(rows)

    # Send a flash message once the export is done
    flash('CSV export completed!', 'success')
