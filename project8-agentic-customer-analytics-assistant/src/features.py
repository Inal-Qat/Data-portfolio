# features engineering, adding new features to the dataset
import pandas as pd


def add_engineered_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add engineered features to the customer analytics dataframe:
    - Recency
    - Frequency
    - CustomerTotalRevenue
    - CustomerAvgRevenue
    - CategoryReturnRate
    - ReturnFlag
    """
    df = df.copy()

    # Parse datetime columns if present
    date_cols = ["SessionStart", "SessionEnd", "CartAdditionTime", "OrderConfirmationTime"]
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    # Recency: days since last session
    if "SessionEnd" in df.columns:
        df["Recency"] = (df["SessionEnd"].max() - df["SessionEnd"]).dt.days

    # Frequency per customer
    if "CustomerID" in df.columns and "OrderReturn" in df.columns:
        freq = df.groupby("CustomerID")["OrderReturn"].count().rename("Frequency")
        df = df.merge(freq, on="CustomerID", how="left")

    # CustomerTotalRevenue & CustomerAvgRevenue
    if "CustomerID" in df.columns and "Revenue" in df.columns:
        customer_revenue = (
            df.groupby("CustomerID")["Revenue"]
            .sum()
            .rename("CustomerTotalRevenue")
        )
        customer_avg_revenue = (
            df.groupby("CustomerID")["Revenue"]
            .mean()
            .rename("CustomerAvgRevenue")
        )
        df = df.merge(customer_revenue, on="CustomerID", how="left")
        df = df.merge(customer_avg_revenue, on="CustomerID", how="left")

    # CategoryReturnRate
    if "Category" in df.columns and "OrderReturn" in df.columns:
        cat_return_rate = (
            df.groupby("Category")["OrderReturn"]
            .mean()
            .rename("CategoryReturnRate")
        )
        df = df.merge(cat_return_rate, on="Category", how="left")

    # ReturnFlag
    if "ReturnReason" in df.columns:
        df["ReturnFlag"] = df["ReturnReason"].notna().astype(int)

    return df