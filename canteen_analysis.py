# ============================================================
# COLLEGE CANTEEN SALES & CUSTOMER SPENDING ANALYSIS
# Team: Abel Joseph & Abhimanue Jijish (25BCAR0055)
# ============================================================

# Required libraries:
# pip install pandas numpy matplotlib

import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ------------------------------------------------------------
# 1. LOAD DATA
# ------------------------------------------------------------

FILE_NAME = "canteen_sales.csv"

df = pd.read_csv(FILE_NAME)

print("=" * 60)
print("COLLEGE CANTEEN SALES & CUSTOMER SPENDING ANALYSIS")
print("=" * 60)

print("\nDataset loaded successfully!")
print("Number of rows:", len(df))
print("Number of columns:", len(df.columns))

print("\nFirst 5 records:")
print(df.head())


# ------------------------------------------------------------
# 2. BASIC DATA INSPECTION
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("2. BASIC DATA INSPECTION")
print("=" * 60)

print("\nColumn names:")
print(list(df.columns))

print("\nMissing values before cleaning:")
print(df.isnull().sum())

print("\nDuplicate rows before cleaning:", df.duplicated().sum())


# ------------------------------------------------------------
# 3. DATA CLEANING
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("3. DATA CLEANING")
print("=" * 60)

# Remove exact duplicate rows
df = df.drop_duplicates().copy()

# Clean text fields
df["Order_ID"] = df["Order_ID"].astype(str).str.strip().str.upper()
df["Item"] = df["Item"].astype(str).str.strip().str.title()
df["Category"] = df["Category"].astype("string").str.strip().str.title()
df["Payment_Method"] = (
    df["Payment_Method"]
    .astype("string")
    .str.strip()
    .str.upper()
)

# Convert numeric columns
df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
df["Unit_Price"] = pd.to_numeric(df["Unit_Price"], errors="coerce")

# Fill missing values
df["Category"] = df["Category"].fillna(df["Category"].mode()[0])
df["Payment_Method"] = df["Payment_Method"].fillna(
    df["Payment_Method"].mode()[0]
)
df["Quantity"] = df["Quantity"].fillna(df["Quantity"].median())

# Convert quantity to integer
df["Quantity"] = df["Quantity"].astype(int)

# Convert date
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# Recalculate total amount instead of blindly trusting the raw value
df["Total_Amount"] = df["Quantity"] * df["Unit_Price"]

print("Duplicate rows after cleaning:", df.duplicated().sum())

print("\nMissing values after cleaning:")
print(df.isnull().sum())


# ------------------------------------------------------------
# 4. REGULAR EXPRESSIONS
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("4. REGULAR EXPRESSION VALIDATION")
print("=" * 60)

# Valid Order ID format: ORD followed by exactly four digits
order_id_pattern = r"^ORD\d{4}$"

df["Valid_Order_ID"] = df["Order_ID"].str.match(
    order_id_pattern,
    na=False
)

valid_count = df["Valid_Order_ID"].sum()
invalid_count = (~df["Valid_Order_ID"]).sum()

print("Valid Order IDs:", valid_count)
print("Invalid Order IDs:", invalid_count)

if invalid_count > 0:
    print("\nInvalid Order IDs:")
    print(df.loc[~df["Valid_Order_ID"], ["Order_ID"]])
else:
    print("All Order IDs follow the correct format.")


# ------------------------------------------------------------
# 5. PYTHON DATA STRUCTURES
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("5. PYTHON DATA STRUCTURES")
print("=" * 60)

# LIST
food_items = df["Item"].unique().tolist()

# DICTIONARY
item_categories = dict(zip(df["Item"], df["Category"]))

# TUPLE
summary = (
    len(df),
    int(df["Quantity"].sum()),
    float(df["Total_Amount"].sum())
)

print("\nList example - first 5 food items:")
print(food_items[:5])

print("\nDictionary example - item/category:")
for item, category in list(item_categories.items())[:5]:
    print(item, "->", category)

print("\nTuple example - (orders, units sold, revenue):")
print(summary)


# ------------------------------------------------------------
# 6. OBJECT-ORIENTED PROGRAMMING
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("6. OBJECT-ORIENTED PROGRAMMING")
print("=" * 60)


class Order:
    """Represents one canteen order."""

    def __init__(self, order_id, item, quantity, unit_price):
        self.order_id = order_id
        self.item = item
        self.quantity = quantity
        self.unit_price = unit_price

    def total_cost(self):
        return self.quantity * self.unit_price

    def display(self):
        return (
            f"{self.order_id}: {self.quantity} x "
            f"{self.item} = ₹{self.total_cost():.2f}"
        )


# Create an object from the class
sample_order = Order(
    "ORD0001",
    "Coffee",
    2,
    25
)

print("Example Order Object:")
print(sample_order.display())


# ------------------------------------------------------------
# 7. NUMPY ANALYSIS
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("7. NUMPY ANALYSIS")
print("=" * 60)

amounts = df["Total_Amount"].to_numpy()
quantities = df["Quantity"].to_numpy()

average_order = np.mean(amounts)
median_order = np.median(amounts)
minimum_order = np.min(amounts)
maximum_order = np.max(amounts)
standard_deviation = np.std(amounts)
total_units = np.sum(quantities)

print(f"Average order amount: ₹{average_order:.2f}")
print(f"Median order amount: ₹{median_order:.2f}")
print(f"Minimum order amount: ₹{minimum_order:.2f}")
print(f"Maximum order amount: ₹{maximum_order:.2f}")
print(f"Standard deviation: ₹{standard_deviation:.2f}")
print(f"Total units sold: {total_units}")


# ------------------------------------------------------------
# 8. PANDAS DATA PROCESSING
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("8. PANDAS DATA PROCESSING")
print("=" * 60)

# Extract hour from time
df["Hour"] = pd.to_datetime(
    df["Time"],
    format="%H:%M",
    errors="coerce"
).dt.hour

# Extract day name
df["Day"] = df["Date"].dt.day_name()

# Item-level analysis
item_sales = (
    df.groupby("Item", as_index=False)
    .agg(
        Units_Sold=("Quantity", "sum"),
        Revenue=("Total_Amount", "sum")
    )
    .sort_values("Units_Sold", ascending=False)
)

# Category-level analysis
category_sales = (
    df.groupby("Category", as_index=False)
    .agg(
        Orders=("Order_ID", "count"),
        Units_Sold=("Quantity", "sum"),
        Revenue=("Total_Amount", "sum")
    )
    .sort_values("Revenue", ascending=False)
)

# Daily analysis
daily_sales = (
    df.groupby("Date", as_index=False)
    .agg(
        Orders=("Order_ID", "count"),
        Revenue=("Total_Amount", "sum")
    )
    .sort_values("Date")
)

# Hourly analysis
hourly_sales = (
    df.groupby("Hour")
    .agg(
        Orders=("Order_ID", "count"),
        Revenue=("Total_Amount", "sum")
    )
    .sort_index()
)

# Payment method analysis
payment_summary = (
    df.groupby("Payment_Method", as_index=False)
    .agg(
        Orders=("Order_ID", "count"),
        Revenue=("Total_Amount", "sum")
    )
    .sort_values("Orders", ascending=False)
)

print("\nTop 10 items by units sold:")
print(item_sales.head(10).to_string(index=False))

print("\nRevenue by category:")
print(category_sales.to_string(index=False))

print("\nPayment method summary:")
print(payment_summary.to_string(index=False))


# ------------------------------------------------------------
# 9. KEY CALCULATIONS
# ------------------------------------------------------------

top_item = item_sales.iloc[0]
top_category = category_sales.iloc[0]

peak_hour = hourly_sales["Orders"].idxmax()
peak_hour_orders = hourly_sales.loc[peak_hour, "Orders"]

highest_revenue_day = daily_sales.loc[
    daily_sales["Revenue"].idxmax()
]

total_revenue = df["Total_Amount"].sum()
total_orders = len(df)

print("\n" + "=" * 60)
print("9. KEY CALCULATIONS")
print("=" * 60)

print(f"Total orders: {total_orders}")
print(f"Total revenue: ₹{total_revenue:,.2f}")
print(f"Average order value: ₹{average_order:,.2f}")
print(
    f"Most sold item: {top_item['Item']} "
    f"({int(top_item['Units_Sold'])} units)"
)
print(
    f"Highest revenue category: {top_category['Category']} "
    f"(₹{top_category['Revenue']:,.2f})"
)
print(
    f"Peak ordering hour: {peak_hour}:00 "
    f"({int(peak_hour_orders)} orders)"
)
print(
    f"Highest revenue date: "
    f"{highest_revenue_day['Date'].date()} "
    f"(₹{highest_revenue_day['Revenue']:,.2f})"
)


# ------------------------------------------------------------
# 10. VISUALIZATION 1
# TOP 10 MOST SOLD ITEMS
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("10. VISUALIZATIONS")
print("=" * 60)

top_items = item_sales.head(10).sort_values("Units_Sold")

plt.figure(figsize=(10, 6))
plt.barh(top_items["Item"], top_items["Units_Sold"])
plt.xlabel("Units Sold")
plt.ylabel("Food Item")
plt.title("Top 10 Most Sold Canteen Items")
plt.tight_layout()
plt.savefig("01_top_items.png", dpi=150)
plt.show()

print(
    "Insight: This chart shows which food items were purchased "
    "most frequently."
)


# ------------------------------------------------------------
# 11. VISUALIZATION 2
# REVENUE BY CATEGORY
# ------------------------------------------------------------

plt.figure(figsize=(9, 5))
plt.bar(
    category_sales["Category"],
    category_sales["Revenue"]
)
plt.xlabel("Category")
plt.ylabel("Revenue (₹)")
plt.title("Revenue by Food Category")
plt.xticks(rotation=20)
plt.tight_layout()
plt.savefig("02_revenue_by_category.png", dpi=150)
plt.show()

print(
    "Insight: The tallest bar represents the category that "
    "generated the highest revenue."
)


# ------------------------------------------------------------
# 12. VISUALIZATION 3
# DAILY REVENUE
# ------------------------------------------------------------

plt.figure(figsize=(11, 5))
plt.plot(
    daily_sales["Date"],
    daily_sales["Revenue"],
    marker="o"
)
plt.xlabel("Date")
plt.ylabel("Revenue (₹)")
plt.title("Daily Canteen Revenue Trend")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("03_daily_revenue.png", dpi=150)
plt.show()

print(
    "Insight: The line chart shows how revenue changes from "
    "day to day and highlights high and low sales days."
)


# ------------------------------------------------------------
# 13. VISUALIZATION 4
# ORDERS BY HOUR
# ------------------------------------------------------------

plt.figure(figsize=(10, 5))
plt.bar(
    hourly_sales.index.astype(str),
    hourly_sales["Orders"]
)
plt.xlabel("Hour of Day")
plt.ylabel("Number of Orders")
plt.title("Orders by Hour")
plt.tight_layout()
plt.savefig("04_orders_by_hour.png", dpi=150)
plt.show()

print(
    "Insight: This chart identifies the busiest ordering "
    "hours of the day."
)


# ------------------------------------------------------------
# 14. VISUALIZATION 5
# CUSTOMER SPENDING DISTRIBUTION
# ------------------------------------------------------------

plt.figure(figsize=(9, 5))
plt.hist(
    df["Total_Amount"],
    bins=12
)
plt.xlabel("Order Amount (₹)")
plt.ylabel("Number of Orders")
plt.title("Customer Order Spending Distribution")
plt.tight_layout()
plt.savefig("05_spending_distribution.png", dpi=150)
plt.show()

print(
    "Insight: The histogram shows the most common customer "
    "spending range and the spread of order values."
)


# ------------------------------------------------------------
# 15. FINAL FINDINGS
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("15. FINAL FINDINGS")
print("=" * 60)

print(
    f"1. The canteen recorded {total_orders} orders "
    f"with total revenue of ₹{total_revenue:,.2f}."
)

print(
    f"2. The average customer order value was "
    f"₹{average_order:,.2f}."
)

print(
    f"3. {top_item['Item']} was the most sold item with "
    f"{int(top_item['Units_Sold'])} units sold."
)

print(
    f"4. {top_category['Category']} generated the highest "
    f"revenue among the categories."
)

print(
    f"5. The busiest ordering hour was {peak_hour}:00, "
    f"with {int(peak_hour_orders)} orders."
)

print(
    f"6. The highest-revenue day was "
    f"{highest_revenue_day['Date'].date()}, generating "
    f"₹{highest_revenue_day['Revenue']:,.2f}."
)


# ------------------------------------------------------------
# 16. SAVE CLEANED DATA
# ------------------------------------------------------------

cleaned_file = "canteen_sales_cleaned.csv"

df.to_csv(cleaned_file, index=False)

print("\n" + "=" * 60)
print("PROJECT COMPLETED")
print("=" * 60)

print(f"Cleaned dataset saved as: {cleaned_file}")
print("Five visualization images were also saved in this folder.")
print("\nAll major project requirements have been demonstrated:")
print("- Python programming")
print("- Data structures")
print("- Object-Oriented Programming")
print("- Regular Expressions")
print("- NumPy")
print("- Pandas")
print("- Data analysis")
print("- Data visualization")
