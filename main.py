from pathlib import Path
from datetime import datetime, timedelta

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ============================================================================
# CONFIGURATION & LANGUAGE SETUP
# ============================================================================

TEXT = {
    "en": {
        "app_title": "Sales Dashboard",
        "language": "Language / Idioma",
        "register_sale": "Register a sale",
        "date": "Date",
        "seller": "Seller",
        "product": "Product",
        "quantity": "Quantity",
        "amount": "Sale amount (BRL)",
        "register_button": "Register sale",
        "sale_registered": "Sale registered!",
        "sales_history": "Sales history",
        "insights": "📊 Performance Insights",
        "filters": "🔍 Filters",
        "dashboard": "Dashboard",
        "total_revenue": "Total Revenue",
        "total_sales": "Total Sales",
        "avg_ticket": "Average Ticket",
        "top_seller": "Top Seller",
        "revenue_by_seller": "Revenue by Seller",
        "revenue_by_product": "Revenue by Product",
        "sales_trend": "Sales Trend Over Time",
        "seller_comparison": "Seller Performance Comparison",
        "chart_amount": "Revenue (BRL)",
        "date_range": "Date Range",
        "selected_sellers": "Select Sellers",
        "selected_products": "Select Products",
        "clear_filters": "Clear Filters",
        "growth_rate": "Growth Rate (MoM)",
        "ticket_details": "Ticket Details by Seller",
    },
    "pt": {
        "app_title": "Painel de Vendas",
        "language": "Language / Idioma",
        "register_sale": "Cadastrar venda",
        "date": "Data",
        "seller": "Vendedor",
        "product": "Produto",
        "quantity": "Quantidade",
        "amount": "Valor da venda (BRL)",
        "register_button": "Cadastrar venda",
        "sale_registered": "Venda cadastrada!",
        "sales_history": "Histórico de vendas",
        "insights": "📊 Análise de Performance",
        "filters": "🔍 Filtros",
        "dashboard": "Dashboard",
        "total_revenue": "Faturamento Total",
        "total_sales": "Total de Vendas",
        "avg_ticket": "Ticket Médio",
        "top_seller": "Melhor Vendedor",
        "revenue_by_seller": "Faturamento por Vendedor",
        "revenue_by_product": "Faturamento por Produto",
        "sales_trend": "Tendência de Vendas",
        "seller_comparison": "Comparação de Performance",
        "chart_amount": "Faturamento (BRL)",
        "date_range": "Período",
        "selected_sellers": "Selecione Vendedores",
        "selected_products": "Selecione Produtos",
        "clear_filters": "Limpar Filtros",
        "growth_rate": "Taxa de Crescimento (MoM)",
        "ticket_details": "Detalhes do Ticket por Vendedor",
    },
}

PRODUCT_NAMES = {
    "Laptop": {"en": "Laptop", "pt": "Notebook"},
    "Cell phone": {"en": "Cell phone", "pt": "Celular"},
    "Headphones": {"en": "Headphones", "pt": "Fone"},
}

# ============================================================================
# PAGE CONFIG & LANGUAGE SELECTION
# ============================================================================

st.set_page_config(
    page_title="Sales Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

language_options = {"English": "en", "Português": "pt"}
selected_language = st.sidebar.selectbox(
    TEXT["en"]["language"], options=list(language_options)
)
language = language_options[selected_language]
text = TEXT[language]

st.title(text["app_title"])

# ============================================================================
# DATA LOADING
# ============================================================================

sales_file = Path(__file__).resolve().parent / "sales.csv"
sales = pd.read_csv(sales_file)
sales["date"] = pd.to_datetime(sales["date"])

# Create localized product names for display
product_labels = {
    product: names[language] for product, names in PRODUCT_NAMES.items()
}

# ============================================================================
# SIDEBAR: REGISTER NEW SALE
# ============================================================================

with st.sidebar:
    st.markdown("---")
    st.subheader(text["register_sale"])
    
    sale_date = st.date_input(text["date"])
    seller = st.selectbox(text["seller"], ["Ana", "Bruno", "Carla"])
    selected_product_label = st.selectbox(
        text["product"], list(product_labels.values())
    )
    product = next(
        key for key, label in product_labels.items() if label == selected_product_label
    )
    quantity = st.number_input(text["quantity"], min_value=1, step=1)
    amount = st.number_input(
        text["amount"], min_value=0.01, step=0.01, format="%.2f"
    )
    
    register_clicked = st.button(text["register_button"], use_container_width=True)
    
    if register_clicked:
        new_sale = [pd.Timestamp(sale_date), seller, product, quantity, amount]
        sales.loc[len(sales)] = new_sale
        sales.to_csv(sales_file, index=False)
        st.success(text["sale_registered"])
        st.rerun()

# ============================================================================
# FILTERS (DATA ANALYST FOCUSED)
# ============================================================================

with st.sidebar:
    st.markdown("---")
    st.subheader(text["filters"])
    
    # Date range filter
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input(
            "From", value=sales["date"].min(), label_visibility="collapsed"
        )
    with col2:
        end_date = st.date_input(
            "To", value=sales["date"].max(), label_visibility="collapsed"
        )
    
    # Seller filter
    selected_sellers = st.multiselect(
        text["selected_sellers"],
        options=sorted(sales["seller"].unique()),
        default=sorted(sales["seller"].unique()),
    )
    
    # Product filter
    selected_products = st.multiselect(
        text["selected_products"],
        options=sorted(sales["product"].unique()),
        default=sorted(sales["product"].unique()),
    )
    
    # Apply filters
    filtered_sales = sales[
        (sales["date"].dt.date >= start_date)
        & (sales["date"].dt.date <= end_date)
        & (sales["seller"].isin(selected_sellers))
        & (sales["product"].isin(selected_products))
    ].copy()

# ============================================================================
# KPI CARDS (TOP METRICS)
# ============================================================================

st.subheader(text["insights"])

# Calculate metrics
total_revenue = filtered_sales["amount"].sum()
total_transactions = len(filtered_sales)
avg_ticket = filtered_sales["amount"].mean() if total_transactions > 0 else 0
top_seller = (
    filtered_sales.groupby("seller")["amount"].sum().idxmax()
    if total_transactions > 0
    else "—"
)

# Format currency for display
def format_currency(value):
    if language == "pt":
        return f"R$ {value:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")
    else:
        return f"R$ {value:,.2f}"

# Display KPI cards
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(text["total_revenue"], format_currency(total_revenue))

with col2:
    st.metric(text["total_sales"], f"{total_transactions:,}")

with col3:
    st.metric(text["avg_ticket"], format_currency(avg_ticket))

with col4:
    st.metric(text["top_seller"], top_seller)

# ============================================================================
# DATA VISUALIZATIONS (ANALYTICS FOCUS)
# ============================================================================

st.markdown("---")

# 1. REVENUE BY SELLER (with trend)
col1, col2 = st.columns(2)

with col1:
    localized_sales = filtered_sales.copy()
    localized_sales["product"] = localized_sales["product"].map(product_labels)
    
    revenue_by_seller = filtered_sales.groupby("seller", as_index=False)["amount"].sum()
    revenue_by_seller = revenue_by_seller.sort_values("amount", ascending=True)
    
    fig_seller = px.bar(
        revenue_by_seller,
        x="amount",
        y="seller",
        orientation="h",
        title=text["revenue_by_seller"],
        labels={
            "seller": text["seller"],
            "amount": text["chart_amount"],
        },
        color="amount",
        color_continuous_scale="Blues",
    )
    fig_seller.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig_seller, use_container_width=True)

# 2. REVENUE BY PRODUCT (pie chart)
with col2:
    revenue_by_product = filtered_sales.groupby("product", as_index=False)["amount"].sum()
    revenue_by_product["product_localized"] = revenue_by_product["product"].map(
        product_labels
    )
    
    fig_product = px.pie(
        revenue_by_product,
        names="product_localized",
        values="amount",
        title=text["revenue_by_product"],
        labels={"product_localized": text["product"], "amount": text["chart_amount"]},
    )
    fig_product.update_layout(height=400)
    st.plotly_chart(fig_product, use_container_width=True)

# 3. SALES TREND OVER TIME
localized_sales["product"] = localized_sales["product"].map(product_labels)
daily_sales = filtered_sales.groupby("date", as_index=False)["amount"].sum()

fig_trend = px.line(
    daily_sales,
    x="date",
    y="amount",
    title=text["sales_trend"],
    labels={
        "date": text["date"],
        "amount": text["chart_amount"],
    },
    markers=True,
)
fig_trend.update_layout(height=400, hovermode="x unified")
st.plotly_chart(fig_trend, use_container_width=True)

# 4. SELLER COMPARISON (grouped bar chart)
revenue_by_seller_product = filtered_sales.groupby(
    ["seller", "product"], as_index=False
)["amount"].sum()
revenue_by_seller_product["product_localized"] = revenue_by_seller_product[
    "product"
].map(product_labels)

fig_comparison = px.bar(
    revenue_by_seller_product,
    x="seller",
    y="amount",
    color="product_localized",
    barmode="group",
    title=text["seller_comparison"],
    labels={
        "seller": text["seller"],
        "product_localized": text["product"],
        "amount": text["chart_amount"],
    },
)
fig_comparison.update_layout(height=400)
st.plotly_chart(fig_comparison, use_container_width=True)

# 5. TICKET DETAILS BY SELLER (statistics table)
st.subheader(text["ticket_details"])

seller_stats = filtered_sales.groupby("seller").agg({
    "amount": ["count", "sum", "mean", "min", "max"],
}).round(2)
seller_stats.columns = [
    text["total_sales"],
    text["total_revenue"],
    text["avg_ticket"],
    "Min",
    "Max"
]
seller_stats = seller_stats.reset_index()
seller_stats = seller_stats.rename(columns={"seller": text["seller"]})

st.dataframe(seller_stats, use_container_width=True)

# ============================================================================
# DETAILED SALES HISTORY
# ============================================================================

st.markdown("---")
st.subheader(text["sales_history"])

display_columns = {
    "date": text["date"],
    "seller": text["seller"],
    "product": text["product"],
    "quantity": text["quantity"],
    "amount": text["amount"],
}

sales_display = localized_sales.rename(columns=display_columns)
st.dataframe(sales_display, use_container_width=True)
