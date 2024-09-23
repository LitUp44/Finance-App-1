import streamlit as st
import pandas as pd
import plotly.express as px

def calculate_fixed_expense_ratio(income, fixed_expenses):
    if income == 0:
        return 0
    return (fixed_expenses / income) * 100

def get_ratio_message(ratio):
    if ratio > 80:
        return "Your fixed expenses are quite high compared to your income. This can result in anxiety or stress as well as missing your goals."
    elif 60 <= ratio <= 80:
        return "Your fixed expenses are on the higher side but manageable, especially if you live in a high cost of living area or have a young family."
    else:
        return "You have a great fixed expense ratio leaving lots of money for play and investing."

def create_pie_chart(data, title, colors=None):
    fig = px.pie(
        names=list(data.keys()),
        values=list(data.values()),
        title=title,
        color_discrete_sequence=colors
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(showlegend=False)
    return fig

def create_bar_chart(data, title):
    fig = px.bar(
        x=list(data.keys()),
        y=list(data.values()),
        title=title,
        labels={'x': 'Category', 'y': 'Amount ($)'},
        text=[f'${value:.2f}' for value in data.values()],
    )
    fig.update_traces(marker_color='#2e6ef7', textposition='outside')
    fig.update_layout(xaxis_tickangle=-45)
    return fig

def main():
    # Apply custom styles
    st.markdown(
        """
        <style>
        /* Background color */
        .stApp {
            background-color: #f0f2f6;
            background-image: url('https://your-image-url.com/image.jpg');
            background-size: cover;
        }
        /* Title color */
        h1 {
            color: #2e6ef7;
        }
        /* Subheader color */
        h2 {
            color: #2e6ef7;
        }
        /* Button styling */
        .stButton>button {
            color: white;
            background-color: #2e6ef7;
            border-radius: 5px;
            padding: 0.5em 1em;
        }
        /* Input styling */
        input {
            border: 1px solid #2e6ef7;
            border-radius: 5px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("Personal Finance Tracker 💰")

    # Add descriptive text below the title
    st.write("""
    In this section we want to help understand you - today! What do you like & want to do with your money that helps you live the life you want to live today.

    We will look at your big picture money allocation as well as your categories to give some insights on how you may be feeling month to month. This will let you discover where you can play around more with your long-term vision as well as how you can optimise this month or this year.

    For this first section: please reference your last three months of income & spending to average a normal month. Checking your credit card / debit card bills is a great way to go. We find this also makes it easier to be honest with expenses. In the second section you can break it down into rough groups to see how it usually plays out in smaller categories.

    Before we get into the next section: there is no right or wrong ratio it depends on how much you already have in savings and investments but for reference usually if savings + investments is less than 10% you may be limited in what you can do in your ‘Future You’. But don’t worry - we’ll get there!
    """)

    # Initialize session state variables
    if 'total_expenses' not in st.session_state:
        st.session_state.total_expenses = 0.0
    if 'monthly_income' not in st.session_state:
        st.session_state.monthly_income = 0.0
    if 'savings' not in st.session_state:
        st.session_state.savings = 0.0
    if 'investments' not in st.session_state:
        st.session_state.investments = 0.0
    if 'fixed_expenses' not in st.session_state:
        st.session_state.fixed_expenses = []
    if 'variable_expenses' not in st.session_state:
        st.session_state.variable_expenses = []

    # First Section: Overview
    st.header("Monthly Overview")
    col1, col2 = st.columns(2)
    with col1:
        monthly_income = st.number_input("Enter your monthly income:", min_value=0.0, step=100.0)
        st.session_state.monthly_income = monthly_income
        savings = st.number_input("Amount allocated to savings:", min_value=0.0, step=10.0)
        st.session_state.savings = savings

    with col2:
        investments = st.number_input("Amount allocated to investments:", min_value=0.0, step=10.0)
        st.session_state.investments = investments
        total_expenses = st.number_input("Total monthly expenses:", min_value=0.0, step=10.0)
        st.session_state.total_expenses = total_expenses

    # Calculate and display results for the first section
    if st.button("Calculate Overview"):
        total_allocations = savings + investments + total_expenses

        st.subheader("Results")
        st.write(f"**Total Monthly Income:** ${monthly_income:.2f}")
        st.write(f"**Total Allocations:** ${total_allocations:.2f}")
        st.write(f"**Difference:** ${monthly_income - total_allocations:.2f}")

        # Calculate savings and investments percentage
        if monthly_income == 0:
            savings_investments_percentage = 0
        else:
            savings_investments_percentage = ((savings + investments) / monthly_income) * 100

        # Determine pie chart colors based on savings + investments percentage
        if savings_investments_percentage > 10:
            colors = ['#a1d99b', '#74c476', '#31a354']
        elif 5 < savings_investments_percentage <= 10:
            colors = ['#fed976', '#feb24c', '#fd8d3c']
        else:
            colors = ['#fc9272', '#fb6a4a', '#de2d26']

        # Pie chart for income allocation
        income_data = {
            'Savings': savings,
            'Investments': investments,
            'Expenses': total_expenses,
        }
        unallocated = max(0, monthly_income - total_allocations)
        if unallocated > 0:
            income_data['Unallocated'] = unallocated
            colors.append('#969696')  # Add color for 'Unallocated'

        fig = create_pie_chart(income_data, 'Income Allocation', colors=colors)
        st.plotly_chart(fig)

    # Second Section: Expense Breakdown
    st.header("Expense Breakdown")
    st.write("""
    Now let’s move to part 2: how do your expenses break down across categories. As with the first section, averaging over 3 months will give you an honest look at how you normally spend money.
    """)
    st.subheader("Fixed Expenses")

    # Fixed expenses default categories
    fixed_expenses_data = {}
    fixed_categories = ['Housing', 'Utilities', 'Insurance', 'Transportation', 'Debt Payments', 'Groceries']
    for category in fixed_categories:
        amount = st.number_input(f"{category}:", min_value=0.0, step=10.0)
        fixed_expenses_data[category] = amount

    # Initialize counters for additional expenses
    if 'fixed_counter' not in st.session_state:
        st.session_state.fixed_counter = 0
    if 'variable_counter' not in st.session_state:
        st.session_state.variable_counter = 0

    # Function to add new fixed expense
    if st.button("➕ Add Fixed Expense Category"):
        st.session_state.fixed_counter += 1

    # Display additional fixed expense inputs
    for i in range(st.session_state.fixed_counter):
        extra_category = st.text_input(f"Fixed Expense Category {i+1} Name:", key=f"fixed_extra_name_{i}")
        extra_amount = st.number_input(f"{extra_category} Amount:", min_value=0.0, step=10.0, key=f"fixed_extra_amount_{i}")
        if extra_category:
            fixed_expenses_data[extra_category] = extra_amount

    st.subheader("Variable Expenses")

    # Variable expenses default categories
    variable_expenses_data = {}
    variable_categories = ['Fun (trips, vacations etc.)']
    for category in variable_categories:
        amount = st.number_input(f"{category}:", min_value=0.0, step=10.0)
        variable_expenses_data[category] = amount

    # Function to add new variable expense
    if st.button("➕ Add Variable Expense Category"):
        st.session_state.variable_counter += 1

    # Display additional variable expense inputs
    for i in range(st.session_state.variable_counter):
        extra_category = st.text_input(f"Variable Expense Category {i+1} Name:", key=f"variable_extra_name_{i}")
        extra_amount = st.number_input(f"{extra_category} Amount:", min_value=0.0, step=10.0, key=f"variable_extra_amount_{i}")
        if extra_category:
            variable_expenses_data[extra_category] = extra_amount

    # Calculate and display results for the second section
    if st.button("Calculate Expenses"):
        # Combine expenses
        expense_data = {**fixed_expenses_data, **variable_expenses_data}
        calculated_total_expenses = sum(expense_data.values())

        if abs(calculated_total_expenses - st.session_state.total_expenses) > 0.01:  # Allow for small floating-point differences
            st.warning(f"The sum of your expenses (${calculated_total_expenses:.2f}) does not match the total expenses you entered (${st.session_state.total_expenses:.2f}). Please adjust your entries.")
        else:
            fixed_expenses_total = sum(fixed_expenses_data.values())
            variable_expenses_total = sum(variable_expenses_data.values())
            fixed_expense_ratio = calculate_fixed_expense_ratio(st.session_state.monthly_income, fixed_expenses_total)

            st.subheader("Fixed Expense Totals")
            st.write(f"Your total fixed expenses are: **${fixed_expenses_total:.2f}**")

            st.subheader("Fixed Expense Ratio")
            st.write(f"Your fixed expense ratio is: **{fixed_expense_ratio:.2f}%**")
            st.write(get_ratio_message(fixed_expense_ratio))

            # Bar chart for expense breakdown
            fig = create_bar_chart(expense_data, 'Expense Breakdown')
            st.plotly_chart(fig)

            # Create a new pie chart with savings + investments, fixed expenses, variable expenses, unallocated
            total_income = st.session_state.monthly_income
            savings_investments = st.session_state.savings + st.session_state.investments
            unallocated = max(0, total_income - (savings_investments + calculated_total_expenses))
            allocation_data = {
                'Savings + Investments': savings_investments,
                'Fixed Expenses': fixed_expenses_total,
                'Variable Expenses': variable_expenses_total,
            }
            colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
            if unallocated > 0:
                allocation_data['Unallocated'] = unallocated
                colors.append('#969696')

            fig2 = create_pie_chart(allocation_data, 'Income and Expenses Allocation', colors=colors)
            st.plotly_chart(fig2)

            # Display insights text
            st.write("""
            **Insights:**

            Fixed expenses: Usually if your fixed expenses, the expenses you can’t easily change month to month, are more than 60-70% of your total take-home income you can feel anxiety around your money. This is because you have less and less to play with when big expenses come up, you over exceed your usual spending in a small category, like groceries, or feel that the money is going out as quickly as it’s coming in.

            Savings & Investing: A great rule of thumb is to save 10-20% of your income. Once you’ve maxed out your rainy day savings (3-6 months of your income) you can switch almost all of that money to long-term investments.

            Fun money! This is the money that can make life feel worth living. Be that shopping, vacations, your morning Starbucks; this is your money to do what you want with that changes month-to-month. Our finger in the air suggestion is somewhere around 10-30% of your take home income.
            """)

            # Calculate savings and investments percentage
            if total_income == 0:
                savings_investments_percentage = 0
            else:
                savings_investments_percentage = ((savings_investments) / total_income) * 100

            # Display the appropriate message based on the user's financial ratios
            if savings_investments_percentage >= 10 and fixed_expense_ratio <= 70:
                st.write("**Well done, you're within this range!**")
            elif savings_investments_percentage >= 10 or fixed_expense_ratio <= 70:
                st.write("**You are close to hitting this goal.**")
            elif savings_investments_percentage <= 5 and fixed_expense_ratio >= 75:
                st.write("**Getting closer to the goal might improve how you feel about money day-to-day.**")
            else:
                st.write("**Keep working towards your financial goals!**")

if __name__ == "__main__":
    main()

