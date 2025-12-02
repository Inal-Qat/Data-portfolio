import os
import sys
from typing import Dict, Any

import streamlit as st
import pandas as pd

# --- Make src importable (same trick as in notebooks) ---
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

# --- Import your project modules ---
from src.data_tools import df  # dataset with engineered features
from src.model_tools import model  # trained RF pipeline
from src.agent_langgraph import run_graph_agent


# ---------- Helpers ----------

def predict_return_from_row(idx: int) -> Dict[str, Any]:
    """Run the RF model on an existing order row and return prob + label."""

    # Use the SAME feature selection logic as in training (notebook 2)
    drop_cols = [
        "FullName",
        "ReturnReason",
        "SessionStart",
        "SessionEnd",
        "CartAdditionTime",
        "OrderConfirmationTime",
    ]
    drop_cols = [c for c in drop_cols if c in df.columns]

    target_col = "OrderReturn" if "OrderReturn" in df.columns else None

    cols_to_drop = drop_cols + ([target_col] if target_col else [])
    feature_cols = [c for c in df.columns if c not in cols_to_drop]

    # Build a one-row DataFrame with the exact feature columns
    X_new = df.loc[[idx], feature_cols]

    # Predict with the trained pipeline
    proba = float(model.predict_proba(X_new)[0, 1])
    pred = int(model.predict(X_new)[0])
    label = "Return" if pred == 1 else "No return"

    # For display, we can still show the full original row as "features"
    features = df.loc[idx].to_dict()

    return {
        "probability": proba,
        "label": label,
        "features": features,
    }


def compute_basic_insights() -> Dict[str, Any]:
    """Precompute some dataset insights for the Insights tab."""
    out: Dict[str, Any] = {}

    if "OrderReturn" in df.columns:
        out["overall_return_rate"] = float(df["OrderReturn"].mean())

    if "Category" in df.columns and "OrderReturn" in df.columns:
        cat_rates = (
            df.groupby("Category")["OrderReturn"]
            .mean()
            .sort_values(ascending=False)
        )
        out["return_rate_by_category"] = cat_rates

    if "Product" in df.columns and "OrderReturn" in df.columns:
        prod_rates = (
            df.groupby("Product")["OrderReturn"]
            .mean()
            .sort_values(ascending=False)
        )
        out["top_products_by_return"] = prod_rates.head(10)

    if "CustomerID" in df.columns and "Revenue" in df.columns:
        top_customers = (
            df.groupby("CustomerID")["Revenue"]
            .sum()
            .sort_values(ascending=False)
        )
        out["top_customers"] = top_customers.head(10)

    return out


# ---------- Streamlit UI ----------

st.set_page_config(
    page_title="Agentic Customer Analytics Assistant",
    layout="wide",
)

st.title("🧠 Agentic Customer Analytics Assistant")
st.caption(
    "Project 8 – ML + LangGraph + Groq-powered analytics on a synthetic e-commerce dataset."
)

# Tabs: Prediction | Insights | AI Agent
tab_pred, tab_insights, tab_agent = st.tabs(
    ["🎯 Return Risk Prediction", "📊 Dataset Insights", "🤖 AI Analytics Agent"]
)

# ---------- Tab 1: Return Risk Prediction ----------

with tab_pred:
    st.subheader("🎯 Predict Return Risk for an Existing Order")

    st.write(
        "Select an existing order from the dataset. "
        "The app will run the trained RandomForest model to estimate return risk."
    )

    # Let user pick an order by index with some helpful label
    df_display = df.reset_index().rename(columns={"index": "RowIndex"})
    df_display["label"] = (
        "Row "
        + df_display["RowIndex"].astype(str)
        + " | Customer "
        + df_display["CustomerID"].astype(str)
        + " | "
        + df_display["Category"].astype(str)
        + " - "
        + df_display["Product"].astype(str)
    )

    selected_label = st.selectbox(
        "Select an example order:",
        options=df_display["label"],
    )

    # Map back to row index
    selected_row_idx = int(
        df_display.loc[df_display["label"] == selected_label, "RowIndex"].iloc[0]
    )

    st.markdown("**Selected order details:**")
    st.dataframe(df.iloc[[selected_row_idx]])

    if st.button("🔍 Predict return risk for this order"):
        with st.spinner("Running model prediction..."):
            result = predict_return_from_row(selected_row_idx)

        prob = result["probability"]
        label = result["label"]

        st.markdown(
            f"### Prediction\n"
            f"- **Predicted label:** `{label}`\n"
            f"- **Estimated return probability:** `{prob:.3f}`"
        )
        st.info(
            "⚠️ The model is intentionally weak (ROC-AUC ≈ 0.50). "
            "Treat this as a rough risk indicator, not a precise forecast. "
            "This is realistic for many imbalanced business problems."
        )


# ---------- Tab 2: Dataset Insights ----------

with tab_insights:
    st.subheader("📊 Dataset Insights")

    insights = compute_basic_insights()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Overall Return Rate")
        overall = insights.get("overall_return_rate", None)
        if overall is not None:
            st.metric("Overall return rate", f"{overall:.3f}")
        else:
            st.write("OrderReturn column not found.")

        st.markdown("#### Return Rate by Category")
        cat_rates = insights.get("return_rate_by_category", None)
        if cat_rates is not None:
            st.dataframe(cat_rates.rename("ReturnRate"))
        else:
            st.write("No category-level data available.")

    with col2:
        st.markdown("#### Top 10 Products by Return Rate")
        top_prod = insights.get("top_products_by_return", None)
        if top_prod is not None:
            st.dataframe(top_prod.rename("ReturnRate"))
        else:
            st.write("No product-level return data available.")

        st.markdown("#### Top 10 Customers by Revenue")
        top_cust = insights.get("top_customers", None)
        if top_cust is not None:
            st.dataframe(top_cust.rename("TotalRevenue"))
        else:
            st.write("No customer revenue data available.")

    st.markdown("---")
    st.caption(
        "These insights are computed directly from the dataset and can be used along with the agent for deeper analysis."
    )


# ---------- Tab 3: AI Analytics Agent (LangGraph) ----------

with tab_agent:
    st.subheader("🤖 AI Analytics Agent (LangGraph + Groq)")

    st.write(
        "Ask questions about returns, customers, and the dataset. "
        "The agent uses tools (EDA functions + the ML model) behind the scenes."
    )

    # Simple chat-like UI (stateless per question)
    user_query = st.text_area(
        "Ask the agent a question:",
        placeholder=(
            "Examples:\n"
            "- Which category has the highest return rate and what does that mean?\n"
            "- Summarize the return behavior of electronics vs fashion.\n"
            "- How risky are returns overall in this dataset?\n"
        ),
        height=140,
    )

    if st.button("🧠 Ask Agent"):
        if not user_query.strip():
            st.warning("Please enter a question.")
        else:
            with st.spinner("Thinking with tools (LangGraph + Groq)..."):
                try:
                    answer = run_graph_agent(user_query)
                except Exception as e:
                    answer = f"Something went wrong while calling the agent: {e}"

            st.markdown("### Agent's answer")
            st.write(answer)

    st.markdown("---")
    st.caption(
        "This agent is built with LangGraph on top of LangChain and Groq's `llama-3.1-8b-instant` model, "
        "and uses tools for data analysis and model-based return risk estimation."
    )