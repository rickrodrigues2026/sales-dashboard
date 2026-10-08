from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

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
        "dashboard": "Dashboard",
        "total_revenue": "Total revenue",
        "revenue_by_seller_product": "Revenue by seller and product",
        "revenue_share_by_product": "Revenue share by product",
        "chart_amount": "Revenue (BRL)",
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
        "dashboard": "Painel",
        "total_revenue": "Faturamento total",
        "revenue_by_seller_product": "Faturamento por vendedor e produto",
        "revenue_share_by_product": "Participação no faturamento por produto",
        "chart_amount": "Faturamento (BRL)",
    },
}

PRODUCT_NAMES = {
    "Laptop": {"en": "Laptop", "pt": "Notebook"},
    "Cell phone": {"en": "Cell phone", "pt": "Celular"},
    "Headphones": {"en": "Headphones", "pt": "Fone"},
}

st.set_page_config(page_title="Sales Dashboard", layout="wide")

language_options = {"English": "en", "Português": "pt"}
selected_language = st.sidebar.selectbox(
    "Language / Idioma", options=list(language_options)
)
language = language_options[selected_language]
text = TEXT[language]

st.title(text["app_title"])

sales_file = Path(__file__).resolve().parent / "sales.csv"
sales = pd.read_csv(sales_file)
sales["date"] = pd.to_datetime(sales["date"])

st.sidebar.header(text["register_sale"])
sale_date = st.sidebar.date_input(text["date"])
seller = st.sidebar.selectbox(text["seller"], ["Ana", "Bruno", "Carla"])
product_labels = {
    product: names[language] for product, names in PRODUCT_NAMES.items()
}
selected_product_label = st.sidebar.selectbox(
    text["product"], list(product_labels.values())
)
product = next(
    key for key, label in product_labels.items() if label == selected_product_label
)
quantity = st.sidebar.number_input(text["quantity"], min_value=1, step=1)
amount = st.sidebar.number_input(
    text["amount"], min_value=0.01, step=0.01, format="%.2f"
)
register_clicked = st.sidebar.button(text["register_button"])

if register_clicked:
    new_sale = [pd.Timestamp(sale_date), seller, product, quantity, amount]
    sales.loc[len(sales)] = new_sale
    sales.to_csv(sales_file, index=False)
    st.success(text["sale_registered"])

localized_sales = sales.copy()
localized_sales["product"] = localized_sales["product"].map(product_labels)
display_columns = {
    "date": text["date"],
    "seller": text["seller"],
    "product": text["product"],
    "quantity": text["quantity"],
    "amount": text["amount"],
}

st.subheader(text["sales_history"])
st.dataframe(localized_sales.rename(columns=display_columns), width="stretch")

st.subheader(text["dashboard"])
total_revenue = sales["amount"].sum()
formatted_revenue = f"{total_revenue:,.2f}"
if language == "pt":
    formatted_revenue = formatted_revenue.replace(",", "_").replace(".", ",").replace("_", ".")
st.metric(text["total_revenue"], f"R$ {formatted_revenue}")

revenue_by_seller_product = localized_sales.groupby(
    ["seller", "product"], as_index=False
)["amount"].sum()
bar_chart = px.bar(
    revenue_by_seller_product,
    x="seller",
    y="amount",
    color="product",
    barmode="stack",
    title=text["revenue_by_seller_product"],
    labels={
        "seller": text["seller"],
        "product": text["product"],
        "amount": text["chart_amount"],
    },
)
st.plotly_chart(bar_chart, width="stretch")

revenue_by_product = localized_sales.groupby("product", as_index=False)["amount"].sum()
pie_chart = px.pie(
    revenue_by_product,
    names="product",
    values="amount",
    title=text["revenue_share_by_product"],
    labels={"product": text["product"], "amount": text["chart_amount"]},
)
st.plotly_chart(pie_chart, width="stretch")
