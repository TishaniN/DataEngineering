**E-commerce Dashboard and Repeat Purchaser Prediction**

_What You’ll Need_

Python 3.7+
MySQL Server installed and running
Python libraries (listed in requirements.txt), like streamlit, pandas, sqlalchemy, scikit-learn, plotly, and matplotlib.
Install the required libraries by running:

pip install -r requirements.txt

**_How to Set Up and Run the Project_**

_1. Start by Creating the Database_
Open MySQL: Make sure MySQL is running on your machine. You can use tools like MySQL Workbench or the MySQL command line.
Create the Database: You’ll need a new database called ecommerce_db. Run this command in MySQL:

            CREATE DATABASE ecommerce_db;

Check Your Database Credentials: In the code files, make sure the database login details (like username and password) match your MySQL setup.

_3. Prepare the Data Files_

Get the CSV Files: You’ll need two CSV files:
  customers.csv – contains customer details, like IDs and names.
  orders.csv – contains order details, including order ID, customer ID, total amount, and order date.
Place the Files in the Right Folder:
The script expects these files in a specific folder, like E:\Delivergate\ on Windows. 
If you’re using a different path, update the file paths in the code to match.

_4. Import Data into MySQL_

Run the Import Script:
  This script will create two tables, customers and orders, in the database if they don’t already exist. It will then load data from your CSV files into these tables.
Clean Up the Data:
  The script will handle duplicates, fill in missing customer names if needed, and ensure only valid customer IDs are used in the orders table.
Verify the Data:
  After running the script, check that the customers and orders tables in MySQL have data loaded from the CSVs.

_5. Launch the Dashboard_
Start Streamlit:
  Open a terminal or command prompt, navigate to the folder where app.py (the dashboard file) is located, and type:

          streamlit run app.py

Open the Dashboard in Your Browser:
This should open the dashboard in a new browser tab.
If it doesn’t, go to http://localhost:8501.

_6. Explore the Dashboard Features_

Use the Filters:
Date Range: View orders within a specific date range.
Total Amount Spent: Set a minimum spending threshold to see only customers who spent above a certain amount.
Minimum Number of Orders: Filter by order count to see customers with multiple purchases.
Visualize the Data:
Filtered Orders Data: Displays data based on the selected filters.
Summary Metrics: Shows quick stats like Total Revenue, Unique Customers, and Total Orders.
Top 10 Customers by Revenue: A bar chart of your top spenders.
Revenue Over Time: A line chart tracking monthly revenue trends.

_7. Run the Machine Learning Model_

Purpose of the Model:
  The machine learning model predicts whether a customer is likely to be a repeat purchaser based on their spending and order count.
Run the Model Script:
  Execute the machine learning script to load the data, train the model, and see how it performs.
Results:
  The script will display the model’s accuracy and show a confusion matrix that helps you understand its predictions.
