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
        "app_subtitle": "Real-time sales analytics and performance insights",
        "language": "Language / Idioma",
        "register_sale": "📝 Register a sale",
        "date": "Date",
        "seller": "Seller",
        "product": "Product",
        "quantity": "Quantity",
        "amount": "Sale amount (BRL)",
        "register_button": "Register sale",
        "sale_registered": "✅ Sale registered successfully!",
        "sales_history": "📋 Sales History",
        "insights": "📊 Key Performance Indicators",
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
        "ticket_details": "Ticket Details by Seller",
        "insights_section": "💡 Analytical Insights",
        "top_product": "Top Product",
        "seller_revenue": "{} leads with {} in revenue",
        "product_revenue": "{} accounts for {:.1f}% of total revenue",
        "avg_growth": "Average ticket value is {}",
        "total_transactions": "{} transactions recorded",
    },
    "pt": {
        "app_title": "Painel de Vendas",
        "app_subtitle": "Análise de vendas e insights de performance em tempo real",
        "language": "Language / Idioma",
        "register_sale": "📝 Cadastrar venda",
        "date": "Data",
        "seller": "Vendedor",
        "product": "Produto",
        "quantity": "Quantidade",
        "amount": "Valor da venda (BRL)",
        "register_button": "Cadastrar venda",
        "sale_registered": "✅ Venda cadastrada com sucesso!",
        "sales_history": "📋 Histórico de vendas",
        "insights": "📊 Indicadores Principais",
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
        "ticket_details": "Detalhes do Ticket por Vendedor",
        "insights_section": "💡 Análise de Insights",
        "top_product": "Produto Destaque",
        "seller_revenue": "{} lidera com {} em faturamento",
        "product_revenue": "{} representa {:.1f}% do faturamento total",
        "avg_growth": "O ticket médio é de {}",
        "total_transactions": "{} transações registradas",
    },
}

PRODUCT_NAMES = {
    "Laptop": {"en": "Laptop", "pt": "Notebook"},
    "Cell phone": {"en": "Cell phone", "pt": "Celular"},
    "Headphones": {"en": "Headphones", "pt": "Fone"},
}

# ============================================================================
# PAGE CONFIG & CUSTOM STYLING
# ============================================================================

st.set_page_config(
    page_title="Sales Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"About": "Sales Dashboard v1.0 | Data Analytics Portfolio"}
)

# Custom CSS for professional styling
st.markdown("""
    <style>
    /* Main title styling */
    .main-title {
        text-align: center;
        margin-bottom: 5px;
        font-size: 2.5em;
        font-weight: 700;
        color: #1f1f1f;
    }
    
    .main-subtitle {
        text-align: center;
        margin-bottom: 30px;
        font-size: 1.1em;
        color: #666666;
        font-weight: 400;
    }
    
    /* KPI Card styling */
    .kpi-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .kpi-value {
        font-size: 1.8em;
        font-weight: 700;
        margin: 10px 0;
    }
    
    .kpi-label {
        font-size: 0.9em;
        opacity: 0.9;
        font-weight: 500;
    }
    
    /* Insights box styling */
    .insight-box {
        background-color: #f0f4ff;
        border-left: 4px solid #667eea;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
        font-size: 0.95em;
    }
    
    .insight-box-strong {
        font-weight: 600;
        color: #667eea;
    }
    
    /* Section divider */
    .section-divider {
        margin: 40px 0 20px 0;
    }
    
    /* Dataframe styling */
    .dataframe-container {
        margin-top: 20px;
    }
    
    /* Sidebar styling */
    .sidebar-section {
        margin-bottom: 20px;
        padding-bottom: 20px;
        border-bottom: 1px solid #e0e0e0;
    }
    
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# LANGUAGE SELECTION
# ============================================================================

language_options = {"English": "en", "Português": "pt"}
selected_language = st.sidebar.selectbox(
    "🌍 " + TEXT["en"]["language"], options=list(language_options)
)
language = language_options[selected_language]
text = TEXT[language]

# ============================================================================
# HEADER
# ============================================================================

st.markdown(f"<div class='main-title'>{text['app_title']}</div>", unsafe_allow_html=True)
st.markdown(f"<div class='main-subtitle'>{text['app_subtitle']}</div>", unsafe_allow_html=True)

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
    st.markdown("<div class='sidebar-section'>", unsafe_allow_html=True)
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
    
    register_clicked = st.button(text["register_button"], use_container_width=True, type="primary")
    
    if register_clicked:
        new_sale = [pd.Timestamp(sale_date), seller, product, quantity, amount]
        sales.loc[len(sales)] = new_sale
        sales.to_csv(sales_file, index=False)
        st.success(text["sale_registered"])
        st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================================
# FILTERS (DATA ANALYST FOCUSED)
# ============================================================================

with st.sidebar:
    st.markdown("<div class='sidebar-section'>", unsafe_allow_html=True)
    st.subheader(text["filters"])
    
    # Date range filter
    min_date = sales["date"].min()
    max_date = sales["date"].max()
    
    date_range = st.slider(
        f"📅 {text['date_range']}",
        min_value=min_date,
        max_value=max_date,
        value=(min_date, max_date),
        format="YYYY-MM-DD"
    )
    start_date, end_date = date_range
    
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
        (sales["date"].dt.date >= start_date.date())
        & (sales["date"].dt.date <= end_date.date())
        & (sales["seller"].isin(selected_sellers))
        & (sales["product"].isin(selected_products))
    ].copy()
    
    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def format_currency(value):
    """Format value as currency based on language setting"""
    if language == "pt":
        return f"R$ {value:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")
    else:
        return f"R$ {value:,.2f}"

# ============================================================================
# KPI CARDS (TOP METRICS)
# ============================================================================

st.subheader(text["insights"])

# Calculate metrics
total_revenue = filtered_sales["amount"].sum()
total_transactions = len(filtered_sales)
avg_ticket = filtered_sales["amount"].mean() if total_transactions > 0 else 0

top_seller_row = (
    filtered_sales.groupby("seller")["amount"].sum().idxmax()
    if total_transactions > 0
    else "—"
)
top_seller_value = (
    filtered_sales[filtered_sales["seller"] == top_seller_row]["amount"].sum()
    if total_transactions > 0
    else 0
)

top_product_row = (
    filtered_sales.groupby("product")["amount"].sum().idxmax()
    if total_transactions > 0
    else "—"
)
top_product_value = (
    filtered_sales[filtered_sales["product"] == top_product_row]["amount"].sum()
    if total_transactions > 0
    else 0
)

# Display KPI cards
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class='kpi-container' style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);'>
        <div class='kpi-label'>{text['total_revenue']}</div>
        <div class='kpi-value'>{format_currency(total_revenue)}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class='kpi-container' style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);'>
        <div class='kpi-label'>{text['total_sales']}</div>
        <div class='kpi-value'>{total_transactions:,}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class='kpi-container' style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);'>
        <div class='kpi-label'>{text['avg_ticket']}</div>
        <div class='kpi-value'>{format_currency(avg_ticket)}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class='kpi-container' style='background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);'>
        <div class='kpi-label'>{text['top_seller']}</div>
        <div class='kpi-value'>{top_seller_row}</div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# AUTOMATIC INSIGHTS (TEXT-BASED ANALYSIS)
# ============================================================================

st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
st.subheader(text["insights_section"])

# Generate insight messages
if total_transactions > 0:
    # Seller insight
    seller_revenue_top = filtered_sales.groupby("seller")["amount"].sum()
    seller_percentage = (seller_revenue_top[top_seller_row] / total_revenue * 100) if total_revenue > 0 else 0
    
    # Product insight
    product_revenue_top = filtered_sales.groupby("product")["amount"].sum()
    top_product_localized = product_labels[top_product_row]
    product_percentage = (top_product_value / total_revenue * 100) if total_revenue > 0 else 0
    
    # Seller comparison
    seller_count = len(selected_sellers)
    
    # Build insights
    insights_text = []
    
    # Insight 1: Top Seller
    insights_text.append(
        f"🏆 <span class='insight-box-strong'>{top_seller_row}</span> " +
        f"leads the team with <span class='insight-box-strong'>{format_currency(top_seller_value)}</span> " +
        f"in revenue ({seller_percentage:.1f}% of total)."
    )
    
    # Insight 2: Top Product
    insights_text.append(
        f"📦 <span class='insight-box-strong'>{top_product_localized}</span> " +
        f"is the top-performing product, representing " +
        f"<span class='insight-box-strong'>{product_percentage:.1f}%</span> of total revenue."
    )
    
    # Insight 3: Average Ticket
    insights_text.append(
        f"💰 The average ticket value is " +
        f"<span class='insight-box-strong'>{format_currency(avg_ticket)}</span>, " +
        f"based on {total_transactions} transactions."
    )
    
    # Insight 4: Activity
    insights_text.append(
        f"📊 <span class='insight-box-strong'>{total_transactions}</span> " +
        f"transactions have been recorded in the selected period."
    )
    
    # Display insights
    for insight in insights_text:
        st.markdown(f"<div class='insight-box'>{insight}</div>", unsafe_allow_html=True)

# ============================================================================
# DATA VISUALIZATIONS (ANALYTICS FOCUS)
# ============================================================================

st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

# Prepare localized data
localized_sales = filtered_sales.copy()
localized_sales["product"] = localized_sales["product"].map(product_labels)

# 1. REVENUE BY SELLER (with trend) & 2. REVENUE BY PRODUCT (pie chart)
col1, col2 = st.columns(2)

with col1:
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
    fig_seller.update_layout(
        height=400,
        showlegend=False,
        hovermode="closest",
        margin=dict(l=0, r=0, t=40, b=0)
    )
    fig_seller.update_traces(hovertemplate="<b>%{y}</b><br>Revenue: R$ %{x:,.0f}<extra></extra>")
    st.plotly_chart(fig_seller, use_container_width=True)

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
    fig_product.update_layout(
        height=400,
        margin=dict(l=0, r=0, t=40, b=0)
    )
    fig_product.update_traces(hovertemplate="<b>%{label}</b><br>Revenue: R$ %{value:,.0f}<extra></extra>")
    st.plotly_chart(fig_product, use_container_width=True)

# 3. SALES TREND OVER TIME
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
fig_trend.update_layout(
    height=400,
    hovermode="x unified",
    margin=dict(l=0, r=0, t=40, b=0)
)
fig_trend.update_traces(hovertemplate="<b>%{x|%Y-%m-%d}</b><br>Revenue: R$ %{y:,.0f}<extra></extra>")
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
fig_comparison.update_layout(
    height=400,
    margin=dict(l=0, r=0, t=40, b=0)
)
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
    "Min Value",
    "Max Value"
]
seller_stats = seller_stats.reset_index()
seller_stats = seller_stats.rename(columns={"seller": text["seller"]})

# Format currency columns
for col in [text["total_revenue"], text["avg_ticket"], "Min Value", "Max Value"]:
    seller_stats[col] = seller_stats[col].apply(
        lambda x: f"R$ {x:,.2f}" if pd.notna(x) else "—"
    )

st.dataframe(seller_stats, use_container_width=True, hide_index=True)

# ============================================================================
# DETAILED SALES HISTORY
# ============================================================================

st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
st.subheader(text["sales_history"])

display_columns = {
    "date": text["date"],
    "seller": text["seller"],
    "product": text["product"],
    "quantity": text["quantity"],
    "amount": text["amount"],
}

sales_display = localized_sales.rename(columns=display_columns)
# Add index starting from 1
sales_display = sales_display.reset_index(drop=True)
sales_display.index = sales_display.index + 1

st.dataframe(sales_display, use_container_width=True)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666; font-size: 0.85em; margin-top: 20px;'>"
    "📊 Data Analytics Portfolio | Sales Dashboard v1.0<br>"
    "Built with Python, Streamlit, Pandas & Plotly"
    "</div>",
    unsafe_allow_html=True
)
