# import plotly.graph_objects as go
# from dash import dcc, html

# from django_plotly_dash import DjangoDash

# external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
# app = DjangoDash("dashboard", external_stylesheets=external_stylesheets)

# fig = go.Figure(data=go.Scatter(x=[1, 2, 3], y=[4, 5, 6], mode="lines+markers"))
# app.layout = html.Div(
#     children=[html.H1("Heading"), dcc.Graph(id="prediction-graph", figure=fig)]
# )

import pandas as pd
import plotly.express as px
from dash import dcc, html, dash_table
from django_plotly_dash import DjangoDash
from biapp.models import Receipt, ReceiptItem, Product, Store, Cashier

app = DjangoDash('SalesDashboard')  

def get_dashboard_data():
    receipts = pd.DataFrame.from_records(
        Receipt.objects.values('id', 'timestamp', 'total_amount', 'store', 'cashier')
    )
    receipts['timestamp'] = pd.to_datetime(receipts['timestamp'])

    sales_by_day = receipts.groupby(receipts['timestamp'].dt.date).agg(total_amount=('total_amount', 'sum')).reset_index()
    sales_by_store = receipts.groupby(receipts['store']).agg(total_amount=('total_amount', 'sum')).reset_index()
    store_data = pd.DataFrame(list(Store.objects.values('id', 'location')))
    sales_by_store = sales_by_store.merge(store_data, left_on='store', right_on='id')
    sales_by_store = sales_by_store[['location', 'total_amount']]
    sales_by_store = sales_by_store.sort_values(by='total_amount', ascending=False)
    items = pd.DataFrame.from_records(
        ReceiptItem.objects.values('product', 'quantity')
    ).groupby('product').sum('quantity').reset_index()

    products = pd.DataFrame.from_records(
        Product.objects.values('id', 'name')
    ).rename(columns={'id': 'product'})

    top_products = items.merge(products, on='product').sort_values('quantity', ascending=False).head(10)
    cashier_data = pd.DataFrame(list(Cashier.objects.values('id', 'name')))
    receipts_by_cashier = receipts.groupby('cashier').size().reset_index(name='num_receipts')
    receipts_by_cashier = receipts_by_cashier.merge(cashier_data, left_on='cashier', right_on='id')
    receipts_by_cashier = receipts_by_cashier[['name', 'num_receipts']]
    receipts_by_cashier = receipts_by_cashier.sort_values(by='num_receipts', ascending=False)


    return sales_by_day, sales_by_store, top_products, receipts_by_cashier

sales_by_day, sales_by_store, top_products, receipts_by_cashier = get_dashboard_data()
app.layout = html.Div([
    html.H1('Sales Dashboard', style={'textAlign': 'center'}),
    
    html.Div([
        html.H2('Sales by Day'),
        dcc.Graph(
            figure=px.line(
                sales_by_day,
                x='timestamp',
                y='total_amount',
                title='Sales by Day'
            )
        )
    ]),
    
    html.Div([
        html.H2('Sales by Store'),
        dash_table.DataTable(
            columns=[{'name': col, 'id': col} for col in sales_by_store.columns],
            data=sales_by_store.to_dict('records'),
        )
    ]),
    
    html.Div([
        html.H2('Top Products'),
        dcc.Graph(
            figure=px.bar(
                top_products,
                x='name',
                y='quantity',
                title='Top Products'
            )
        )
    ]),
    
    html.Div([
        html.H2('Receipts by Cashier'),
        dash_table.DataTable(
            columns=[{'name': col, 'id': col} for col in receipts_by_cashier.columns],
            data=receipts_by_cashier.to_dict('records'),
        )
    ])
], style={ "height" : "100vh"})