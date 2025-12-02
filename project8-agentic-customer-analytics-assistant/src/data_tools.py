# load dataset + EDA tools
import os
from typing import List

import pandas as pd
from langchain_core.tools import tool

from .features import add_engineered_features

# Resolve project paths
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")


def load_dataset() -> pd.DataFrame:
    """Load the cleaned CSV and add engineered features."""
    path = os.path.join(DATA_DIR, "customer_analytics_clean.csv")
    df = pd.read_csv(path)
    df = add_engineered_features(df)
    return df


# Load once at import (simple pattern for this project)
df = load_dataset()


@tool
def data_overview(n: int = 5) -> str:
    """Get a general overview of the dataset: shape, columns, numeric summary, and sample rows."""
    info: List[str] = []
    info.append(f"Rows: {len(df)}, Columns: {len(df.columns)}")
    info.append("Columns: " + ", ".join(df.columns))

    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
    if numeric_cols:
        desc = df[numeric_cols].describe().to_string()
        info.append("Numeric summary:\n" + desc)

    sample = df.head(n).to_string()
    info.append(f"Sample {n} rows:\n{sample}")

    return "\n\n".join(info)


@tool
def return_rates() -> str:
    """Analyze overall and category-level return rates in the dataset."""
    if "OrderReturn" not in df.columns:
        return "OrderReturn column not found."

    overall = df["OrderReturn"].mean()
    txt = [f"Overall return rate: {overall:.3f}"]

    if "Category" in df.columns:
        cat_rates = (
            df.groupby("Category")["OrderReturn"]
            .mean()
            .sort_values(ascending=False)
        )
        txt.append("\nReturn rate by Category:\n" + cat_rates.to_string())

    if "Product" in df.columns:
        prod_rates = (
            df.groupby("Product")["OrderReturn"]
            .mean()
            .sort_values(ascending=False)
            .head(10)
        )
        txt.append("\nTop 10 products by return rate:\n" + prod_rates.to_string())

    return "\n\n".join(txt)


@tool
def top_customers(k: int = 10) -> str:
    """List the top-k customers by total revenue."""
    if "CustomerID" not in df.columns or "Revenue" not in df.columns:
        return "CustomerID or Revenue column missing."

    top = (
        df.groupby("CustomerID")["Revenue"]
        .sum()
        .sort_values(ascending=False)
        .head(k)
    )
    return f"Top {k} customers by total revenue:\n{top.to_string()}"