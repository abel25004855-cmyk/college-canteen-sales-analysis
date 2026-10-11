# College Canteen Sales & Customer Spending Analysis

A Python mini project that analyzes simulated college canteen transactions to identify popular food items, revenue patterns, customer spending, and peak ordering hours.

## Project Overview

This project uses Python to clean, process, analyze, and visualize canteen sales data. It demonstrates core programming concepts alongside data analysis libraries.

## Technologies Used

- **Python 3.14**
- **Pandas** for data cleaning and analysis
- **NumPy** for numerical calculations
- **Matplotlib** for data visualization
- **Regular Expressions** for order ID validation
- **Object-Oriented Programming (OOP)** for modeling orders

## Key Findings

Analysis of the cleaned dataset produced these results:

| Metric | Result |
|---|---:|
| Total orders | 600 |
| Total units sold | 894 |
| Total revenue | ₹61,725 |
| Average order value | ₹102.88 |
| Most sold item | Tea, 85 units |
| Highest-revenue category | Lunch, ₹36,930 |
| Busiest ordering hour | 2 PM, 96 orders |
| Most-used payment method | UPI, 409 orders |

## Visualizations

The project generates five graphs:

1. Top 10 most sold canteen items
2. Revenue by food category
3. Daily revenue trend
4. Orders by hour
5. Customer spending distribution

## How to Run

1. Install Python 3.14 or a compatible Python version.
2. Install the required libraries:

   ```bash
   pip install pandas numpy matplotlib
   ```

3. Keep `canteen_analysis.py` and `canteen_sales.csv` in the same folder.
4. Run the program:

   ```bash
   python canteen_analysis.py
   ```

The program prints its findings, generates five graph images, and saves a cleaned CSV file.

## Project Structure

- `canteen_analysis.py` - Main Python program
- `canteen_sales.csv` - Original dataset
- `canteen_sales_cleaned.csv` - Cleaned dataset
- PNG files - Generated visualizations

## Dataset Disclaimer

The dataset is synthetic and was created for educational purposes. The findings represent simulated transactions, not actual sales from a college canteen.

## Authors

- Abel Joseph
- Abhimanue Jijish (25BCAR0055)

**Academic Project:** Python Programming Mini Project
