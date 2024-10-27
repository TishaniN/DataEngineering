import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

# Database connection details
DB_USER = 'root'
DB_PASSWORD = 'Tn20190726!!'
DB_HOST = 'localhost'
DB_PORT = '3306'
DB_NAME = 'ecommerce_db'

# Connect to the database
@st.cache_resource
def connect_db():
    try:
        return create_engine(f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
    except SQLAlchemyError as e:
        st.error(f"Could not connect to database: {e}")
        return None

# Load data from database
@st.cache_data
def load_data(_engine):
    query = """
        SELECT 
            o.order_id, 
            o.customer_id, 
            c.customer_name, 
            o.total_amount, 
            o.order_date
        FROM orders o
        LEFT JOIN customers c ON o.customer_id = c.customer_id
    """
    try:
        df = pd.read_sql(query, _engine)
        df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
        df.dropna(subset=['order_date'], inplace=True)
        return df
    except SQLAlchemyError as e:
        st.error(f"Failed to load data: {e}")
        return pd.DataFrame()

# Connect to the database and load data
engine = connect_db()
df = load_data(engine)

# Check if data loaded successfully
if df.empty:
    st.warning("No data found.")
else:
    st.sidebar.header("Filter Options")

    # Date Range Filter
    min_date, max_date = df['order_date'].min(), df['order_date'].max()
    start_date, end_date = st.sidebar.date_input(
        "Order Date Range",
        [min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )
    # Filter by selected date range
    filtered_df = df[(df['order_date'] >= pd.to_datetime(start_date)) & (df['order_date'] <= pd.to_datetime(end_date))]

    # Total Amount Spent Slider
    total_spent = filtered_df.groupby('customer_id')['total_amount'].sum()
    spent_min, spent_max = int(total_spent.min()), int(total_spent.max())
    spent_threshold = st.sidebar.slider(
        "Minimum Total Amount Spent ($)",
        min_value=spent_min,
        max_value=spent_max,
        value=1000
    )
    # Filter by spending threshold
    eligible_customers = total_spent[total_spent >= spent_threshold].index
    filtered_df = filtered_df[filtered_df['customer_id'].isin(eligible_customers)]

    # Dropdown for Minimum Number of Orders
    order_counts = filtered_df['customer_id'].value_counts()
    max_orders = int(order_counts.max())
    order_threshold = st.sidebar.selectbox(
        "Minimum Number of Orders",
        options=list(range(1, max_orders + 1)),
        index=min(4, max_orders - 1)
    )
    # Filter by order count threshold
    customers_above_order_threshold = order_counts[order_counts >= order_threshold].index
    filtered_df = filtered_df[filtered_df['customer_id'].isin(customers_above_order_threshold)]

    # Main Dashboard
    st.title("E-commerce Dashboard")

    # Display filtered data in a table
    st.subheader("Filtered Orders Data")
    st.dataframe(filtered_df)

    # Summary metrics
    st.subheader("Summary Metrics")
    total_revenue = filtered_df['total_amount'].sum()
    unique_customers = filtered_df['customer_id'].nunique()
    total_orders = filtered_df['order_id'].count()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Revenue", f"${total_revenue:,.2f}")
    col2.metric("Unique Customers", unique_customers)
    col3.metric("Total Orders", total_orders)

    # Bar chart - Top 10 customers by revenue
    st.subheader("Top 10 Customers by Revenue")
    top_customers = filtered_df.groupby('customer_id')['total_amount'].sum().nlargest(10).reset_index()
    top_customers = pd.merge(top_customers, df[['customer_id', 'customer_name']].drop_duplicates(), on='customer_id', how='left')
    fig_bar = px.bar(
        top_customers,
        x='customer_name',
        y='total_amount',
        title="Top 10 Customers by Revenue",
        labels={'total_amount': 'Total Revenue', 'customer_name': 'Customer'}
    )
    st.plotly_chart(fig_bar)

    # Line chart - Total revenue over time (grouped by month)
    st.subheader("Total Revenue Over Time")
    filtered_df['order_month'] = filtered_df['order_date'].dt.to_period('M')
    revenue_over_time = filtered_df.groupby('order_month')['total_amount'].sum().reset_index()
    revenue_over_time['order_month'] = revenue_over_time['order_month'].dt.to_timestamp()
    fig_line = px.line(
        revenue_over_time,
        x='order_month',
        y='total_amount',
        title="Total Revenue Over Time",
        labels={'total_amount': 'Total Revenue', 'order_month': 'Month'}
    )
    st.plotly_chart(fig_line)
