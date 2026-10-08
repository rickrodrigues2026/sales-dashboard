# Sales Dashboard

A bilingual Streamlit application for registering sales, reviewing sales history, and analyzing revenue by seller and product. The interface is available in English and Portuguese.

This project was built as part of Hashtag Treinamentos' Jornada Python and extended with grouped analytics, input validation, bilingual labels, and portfolio documentation.

## Features

- Register sales with a date, seller, product, quantity, and sale amount.
- Browse an interactive sales history.
- Track total revenue.
- Compare revenue by seller and product.
- View each product's share of total revenue.
- Switch the interface between English and Portuguese.

## Tech Stack

- Python
- Streamlit
- Pandas
- Plotly Express

## Run Locally

Requires Python 3.10 or later.

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run main.py
```

The app will be available at `http://localhost:8501`.

## Data and Deployment

Demo sales are stored in `sales.csv`. The `amount` column represents the total value of a sale, not the unit price. Registering a sale updates this CSV file.

The CSV is intended for local demonstration. In a public deployment, visitors may change the shared data, and the hosting service's local storage may be reset. For production use, replace the CSV with persistent database storage and add authentication and access controls.