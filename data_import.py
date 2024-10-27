import pandas as pd
import os
from sqlalchemy import create_engine, text, MetaData, Table, Column, Integer, String, Float, DateTime
from sqlalchemy.exc import SQLAlchemyError
from getpass import getpass

# Database connection parameters
DB_USER = 'root'
DB_PASSWORD = 'Tn20190726!!'
DB_HOST = 'localhost'
DB_PORT = '3306'
DB_NAME = 'ecommerce_db'

# CSV file paths
csv_files = {
    'customers': 'E:\\Delivergate\\customers.csv',
    'orders': 'E:\\Delivergate\\order.csv'
}

# Connect to the database
try:
    engine = create_engine(f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}', echo=False)
    metadata = MetaData()

    # Define tables
    customers_table = Table('customers', metadata,
        Column('customer_id', Integer, primary_key=True),
        Column('customer_name', String(255), nullable=False)
    )
    orders_table = Table('orders', metadata,
        Column('order_id', Integer, primary_key=True),
        Column('customer_id', Integer),
        Column('total_amount', Float, nullable=False),
        Column('order_date', DateTime, nullable=False)
    )

    # Create tables if they do not exist
    metadata.create_all(engine)

    # Import data from CSV if tables are empty
    with engine.connect() as conn:
        # Load, clean, and import customers data
        if conn.execute(text("SELECT COUNT(*) FROM customers")).scalar() == 0:
            customers_df = pd.read_csv(csv_files['customers'])[['customer_id', 'name']].rename(columns={'name': 'customer_name'})
            customers_df['customer_name'] = customers_df['customer_name'].fillna('Unknown')
            customers_df.drop_duplicates(subset=['customer_id'], keep='first', inplace=True)
            customers_df.to_sql('customers', con=engine, if_exists='append', index=False)

        # Load and import orders data
        if conn.execute(text("SELECT COUNT(*) FROM orders")).scalar() == 0:
            orders_df = pd.read_csv(csv_files['orders'])[['id', 'customer_id', 'total_amount', 'created_at']].rename(columns={'id': 'order_id', 'created_at': 'order_date'})
            
            # Fetch existing customer IDs from the customers table
            existing_customer_ids = pd.read_sql("SELECT customer_id FROM customers", con=conn)
            valid_customer_ids = set(existing_customer_ids['customer_id'].astype(int).unique())
            
            # Keep only orders with valid customer_ids
            orders_df['customer_id'] = pd.to_numeric(orders_df['customer_id'], errors='coerce').astype('Int64')
            orders_df = orders_df[orders_df['customer_id'].isin(valid_customer_ids)]
            
            orders_df.to_sql('orders', con=engine, if_exists='append', index=False)
            print("Orders data imported successfully, excluding invalid customer IDs.")

except SQLAlchemyError as e:
    print(f"Database error: {e}")
except Exception as e:
    print(f"Error: {e}")
