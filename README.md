# Sales Dashboard | Painel de Vendas

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.0%2B-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Pandas](https://img.shields.io/badge/Pandas-2.x-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Plotly](https://img.shields.io/badge/Plotly-Interactive-3F4F75?logo=plotly&logoColor=white)](https://plotly.com/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

</div>

A bilingual Streamlit dashboard for registering sales, tracking revenue, and analyzing performance by seller and product.

English | [Português](#português)

---

## English

### Overview

This project is a practical sales management dashboard built with Python and Streamlit. It allows users to register sales, review historical transactions, and view revenue insights by seller and product in a clear and interactive interface.

The application was designed to be simple, intuitive, and easy to understand, while also including a bilingual interface to make the experience accessible to both English and Portuguese speakers.

### Key Features

- Register sales with date, seller, product, quantity, and total amount
- View all recorded sales in an interactive table
- Track total revenue in real time
- Compare revenue by seller and product using grouped analytics
- Visualize product share of revenue with a pie chart
- Switch the app language between English and Portuguese
- Store data locally in a CSV file for easy demo use

### Tech Stack

- Python 3.10+
- Streamlit
- Pandas
- Plotly Express

### Project Goals

- Build a dashboard for small sales monitoring
- Practice Python data processing and business logic
- Create a bilingual interface and modern dashboard experience
- Showcase a portfolio-ready project with clear business relevance

### Run Locally

Requirements: Python 3.10 or later.

```bash
git clone https://github.com/rickrodrigues2026/sales-dashboard.git
cd sales-dashboard
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
# or: .venv\Scripts\Activate.ps1  # Windows PowerShell
python -m pip install -r requirements.txt
streamlit run main.py
```

The app will open at `http://localhost:8501`.

### Project Structure

```text
sales-dashboard/
├── main.py
├── sales.csv
├── requirements.txt
├── README.md
├── .gitignore
└── LICENSE
```

### Notes

The dataset in `sales.csv` is intended for demonstration purposes. It stores sample sales and is updated whenever a new sale is registered. For a production environment, it is recommended to replace the CSV with a database or a more robust storage solution.

### Why This Project Is Portfolio-Ready

This project demonstrates important technical and business-oriented skills:

- data handling with Python and Pandas
- interactive dashboards with Streamlit
- data visualization with Plotly
- multilingual UI design
- practical workflow logic for a business scenario

---

## Português

### Visão Geral

Este projeto é um painel de gestão de vendas construído com Python e Streamlit. Ele permite registrar vendas, revisar o histórico de transações e analisar o faturamento por vendedor e produto em uma interface clara e interativa.

A aplicação foi pensada para ser simples, intuitiva e fácil de entender, além de incluir uma interface bilíngue para tornar a experiência acessível tanto para falantes de inglês quanto de português.

### Funcionalidades Principais

- Registrar vendas com data, vendedor, produto, quantidade e valor total
- Visualizar todas as vendas cadastradas em uma tabela interativa
- Acompanhar o faturamento total em tempo real
- Comparar faturamento por vendedor e produto com análise agrupada
- Visualizar a participação de cada produto no faturamento em gráfico de pizza
- Alternar o idioma do app entre inglês e português
- Armazenar os dados localmente em um arquivo CSV para uso em demonstração

### Stack Tecnológica

- Python 3.10+
- Streamlit
- Pandas
- Plotly Express

### Objetivos do Projeto

- Criar um dashboard para acompanhamento de vendas
- Praticar processamento de dados em Python e lógica de negócio
- Desenvolver uma interface bilíngue e experiência moderna de dashboard
- Apresentar um projeto pronto para portfólio com clara relevância para negócios

### Como Executar Localmente

Requisitos: Python 3.10 ou superior.

```bash
git clone https://github.com/rickrodrigues2026/sales-dashboard.git
cd sales-dashboard
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
# ou: .venv\Scripts\Activate.ps1  # Windows PowerShell
python -m pip install -r requirements.txt
streamlit run main.py
```

A aplicação estará disponível em `http://localhost:8501`.

### Estrutura do Projeto

```text
sales-dashboard/
├── main.py
├── sales.csv
├── requirements.txt
├── README.md
├── .gitignore
└── LICENSE
```

### Observações

O arquivo `sales.csv` foi criado para fins de demonstração. Ele armazena vendas de exemplo e é atualizado sempre que uma nova venda é registrada. Em ambiente de produção, recomenda-se substituir o CSV por um banco de dados ou uma solução mais robusta de armazenamento.

### Por que Este Projeto Vale para Portfólio

Este projeto demonstra habilidades importantes tanto técnicas quanto orientadas a negócios:

- manipulação de dados com Python e Pandas
- dashboards interativos com Streamlit
- visualização de dados com Plotly
- design de interface multilíngue
- lógica prática para cenários empresariais

---

<div align="center">
  <strong>Built with Python • Streamlit • Data Analysis</strong>
</div>
