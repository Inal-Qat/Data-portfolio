#  Project 6 – Sales & Profit Analysis Dashboard (Power BI)

##  Overview
This Power BI dashboard visualizes key sales performance indicators using the **Superstore dataset**.  
The goal is to explore sales, and profit patterns interactively while demonstrating BI and dashboard design skills.

##  Tools & Technologies
- Microsoft Power BI Desktop (October 2025)
- DAX Calculations & Custom Columns
- Interactive Filters (Slicers)
- Data Modeling and Visualization

##  Key Features
- **KPI Cards:** Total Sales, Total Profit, Average Discount 
- **Time Trends:** Sales & Profit over time (month-year view)  
- **Regional Analysis:** Sales & Profit by Region  
- **Product Analysis:** Sales and Profit by Category & Sub-Category  
- **Customer Segmentation:** Sales by Segment and Region  
- **Interactive Filters:** Year, Region, and Category slicers for dynamic insights  
- **Navigation Buttons:** Multi-page layout for Overview, Sales Analysis, and Product Analysis

## Insights
- Profit margin fluctuates seasonally; some months show increased sales but lower profit due to discounts.
- Technology and Office Supplies are top-performing categories in overall revenue.
- Regional differences highlight opportunities for logistic optimization.

##  Example Calculations
```DAX
Profit Margin = DIVIDE([Profit], [Sales], 0)
Shipping Delay = DATEDIFF('Orders'[Order Date], 'Orders'[Ship Date], DAY) (didn't complete yet!)
Order Year = YEAR('Orders'[Order Date])
Month-Year = FORMAT('Orders'[Order Date], "MMM yyyy")