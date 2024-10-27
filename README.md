"# DataEngineering" 

E-commerce Dashboard and Repeat Purchaser Prediction
Overview
This app provides a dashboard to visualize e-commerce data and uses a machine learning model to predict repeat purchasers.
Requirements,
Python 3.7+
MySQL Server
Required Python packages (listed in requirements.txt)
Setup Steps
1. Set Up MySQL Database
   
Start MySQL Server.
Create a database named ecommerce_db (make sure credentials in the code match your MySQL setup).

3. Prepare and Load Data
Place two CSV files, customers.csv and orders.csv, in the specified directory (e.g., E:\Delivergate\).
Run the data import script to:
Create customers and orders tables.
Populate tables with data from the CSV files, clean up duplicates, and validate customer IDs.

5. Start the Dashboard
Open a terminal and navigate to the folder containing the Streamlit app file (e.g., app.py).
Run the command: streamlit run app.py.
The dashboard will open in your web browser.
6. Use the Dashboard
Filter Options:
Filter orders by date range, minimum spending, and minimum number of orders.
Dashboard Features:
Summary Metrics: View total revenue, unique customers, and total orders.
Top 10 Customers: Bar chart showing top-spending customers.
Revenue Over Time: Line chart showing monthly revenue trends.
7. Run the Machine Learning Model
The ML script predicts repeat purchasers.
To use:
Run the machine learning script in your terminal.
The script will:
Load and label customer data.
Train a model on customer spending and order count.
Show model accuracy and a confusion matrix.
