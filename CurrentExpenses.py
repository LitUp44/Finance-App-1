import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# Function to connect to Google Sheets
def connect_to_gsheet():
    # Define the scope
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    
    # Add credentials to the account (replace 'your_credentials_file.json' with the name of your credentials file)
    creds = ServiceAccountCredentials.from_json_keyfile_name('linear-pursuit-436211-u5-0a7f61a7f0e8.json', scope)
    
    # Authorize the clientsheet
    client = gspread.authorize(creds)
    
    # Get the sheet (replace 'your-google-sheet-name' with the actual name of your Google Sheet)
    sheet = client.open('Finance App Output').sheet1
    
    return sheet

# Title for the app
st.title("Monthly Financial Summary App")

# Get user's monthly income
income = st.number_input("What is your monthly income? $", min_value=0.0, step=100.0)

# Get user's savings and investments
savings = st.number_input("How much do you save per month? $", min_value=0.0, step=50.0)
investments = st.number_input("How much do you invest per month? $", min_value=0.0, step=50.0)

st.subheader("Breakdown your monthly expenses")

# Breakdown of fixed expenses
housing = st.number_input("Housing (rent/mortgage): $", min_value=0.0, step=50.0)
utilities = st.number_input("Utilities (electricity, water, internet, etc.): $", min_value=0.0, step=20.0)
insurance = st.number_input("Insurance (health, car, etc.): $", min_value=0.0, step=20.0)
transportation = st.number_input("Transportation (car payment, gas, etc.): $", min_value=0.0, step=20.0)
debt_payments = st.number_input("Debt payments: $", min_value=0.0, step=20.0)
groceries = st.number_input("Groceries: $", min_value=0.0, step=20.0)
clothes = st.number_input("Clothes: $", min_value=0.0, step=20.0)
subscriptions = st.number_input("Subscriptions (phone, streaming, etc.): $", min_value=0.0, step=10.0)
fun = st.number_input("Fun (trips, gifts, dining out, shopping, etc.): $", min_value=0.0, step=20.0)

# Calculate total expenses
total_expenses = (housing + utilities + insurance + transportation + debt_payments +
                  groceries + clothes + subscriptions + fun)

# Calculate remaining balance
remaining_balance = income - (savings + investments + total_expenses)

# Display summary when the user is ready
if st.button("Calculate Summary"):
    st.subheader("Your Monthly Financial Summary")

    st.write(f"**Monthly Income:** ${income:.2f}")
    st.write(f"**Total Savings:** ${savings:.2f}")
    st.write(f"**Total Investments:** ${investments:.2f}")
    st.write(f"**Total Fixed Expenses:** ${total_expenses:.2f}")
    st.write(f"**Remaining Balance:** ${remaining_balance:.2f}")

    # Warning if the expenses exceed income
    if remaining_balance < 0:
        st.warning("Warning: Your expenses exceed your income. Consider adjusting your budget.")
    else:
        st.success("You're on track! You may want to invest more if your balance is positive.")
    
    # Connect to Google Sheet
    sheet = connect_to_gsheet()

    # Prepare data to save
    data = [income, savings, investments, housing, utilities, insurance, transportation,
            debt_payments, groceries, clothes, subscriptions, fun, total_expenses, remaining_balance]
    
    # Save data to the Google Sheet (append the data)
    sheet.append_row(data)

    st.success("Your data has been saved to Google Drive!")
