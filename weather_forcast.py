import streamlit as st
import pandas as pd
import os
from datetime import date


st.title("My Expense Tracker")

if os.path.exists("expenses.csv"):
    df = pd.read_csv("expenses.csv")
else:
    df = pd.DataFrame(
        columns=["amount", "category", "date", "note"]
    )


st.subheader("ADD EXPENSE")

with st.form("expense_form"):

    col1, col2, col3, col4, col5 = st.columns(
        [1, 1, 1, 2, 0.6]
    )

    with col1:
        amount = st.number_input(
            "Amount (₹)",
            min_value=0.0
        )

    with col2:
        category = st.selectbox(
            "Category",
            [
                "Food",
                "Transport",
                "Books",
                "Shopping",
                "Entertainment",
                "Bills",
                "Other"
            ]
        )

    with col3:
        expense_date = st.date_input(
            "Date",
            value=date.today()
        )

    with col4:
        note = st.text_input("Note")

    with col5:
        st.write("")
        st.write("")
        add = st.form_submit_button("Add")


if add:

    new_expense = pd.DataFrame({
        "amount": [amount],
        "category": [category],
        "date": [expense_date],
        "note": [note]
    })

    new_expense.to_csv(
        "expenses.csv",
        mode="a",
        header=not os.path.exists("expenses.csv"),
        index=False
    )

    st.success("Expense added!")

    df = pd.read_csv("expenses.csv")


total = df["amount"].sum() if not df.empty else 0



if not df.empty:

    df["date"] = pd.to_datetime(df["date"])

    this_month = df[
        (df["date"].dt.month == date.today().month) &
        (df["date"].dt.year == date.today().year)
    ]

    month_total = this_month["amount"].sum()

else:

    month_total = 0


col1, col2 = st.columns(2)

with col1:
    st.metric(
        "TOTAL SPENT",
        f"₹ {total:,.0f}"
    )

with col2:
    st.metric(
        "THIS MONTH",
        f"₹ {month_total:,.0f}"
    )

st.subheader("Spending by Category")

if not df.empty:

    category_total = (
        df.groupby("category")["amount"]
        .sum()
    )

    st.bar_chart(category_total)

else:

    st.info("No expenses yet.")



st.subheader("Recent Expenses")

if not df.empty:

    recent = df.sort_values(
        "date",
        ascending=False
    )

    st.dataframe(
        recent,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info("No expenses available.")
