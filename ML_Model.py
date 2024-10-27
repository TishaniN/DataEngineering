# Import necessary libraries
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Database connection details
DB_USER = 'root'
DB_PASSWORD = 'Tn20190726!!'
DB_HOST = 'localhost'
DB_PORT = '3306'
DB_NAME = 'ecommerce_db'

# Connect to the database
def connect_db():
    try:
        return create_engine(f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
    except SQLAlchemyError as e:
        print(f"Could not connect to database: {e}")
        return None

# Establish connection
engine = connect_db()

# Load data from the database
def load_data(engine):
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
        df = pd.read_sql(query, engine)
        df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
        df.dropna(subset=['order_date'], inplace=True)
        return df
    except SQLAlchemyError as e:
        print(f"Failed to load data: {e}")
        return pd.DataFrame()

# Load data
df = load_data(engine)

# Check if data loaded successfully
if df.empty:
    print("No data found.")
else:
    print("Data loaded successfully.")
    print(df.head())

# Preprocess data for machine learning
if not df.empty:
    customer_data = df.groupby('customer_id').agg(
        total_revenue=('total_amount', 'sum'),
        total_orders=('order_id', 'count')
    ).reset_index()

    # Define "repeat purchaser" as customers with more than one order
    customer_data['is_repeat'] = (customer_data['total_orders'] > 1).astype(int)
    
    print(customer_data.head())


# Split data for training and testing
if len(customer_data) < 10:  # Validation check for sufficient data
    print("Not enough data for training the model.")
else:
    X = customer_data[['total_revenue', 'total_orders']]
    y = customer_data['is_repeat']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    print("Data split into training and testing sets.")

# Train Logistic Regression Model
if len(customer_data) >= 10:
    model = LogisticRegression()
    model.fit(X_train, y_train)
    print("Model trained successfully.")


# Model Predictions and Accuracy
if len(customer_data) >= 10:
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print("Model Accuracy: {:.2f}%".format(accuracy * 100))

# Display Sample Predictions
if len(customer_data) >= 10:
    sample_data = X_test.copy()
    sample_data['Predicted Repeat'] = y_pred
    print("Sample Predictions")
    print(sample_data.head())
    
# Import Visualization Libraries
import matplotlib.pyplot as plt
import seaborn as sns

# Set style for the plots
sns.set(style="whitegrid")

# Plot 
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

# Only execute if data length is sufficient for training
if len(customer_data) >= 10:
    # Generate confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    
    # Display confusion matrix
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["Non-repeat", "Repeat"])
    disp.plot(cmap="Blues")
    plt.title("Confusion Matrix - Actual vs Predicted")
    plt.show()
