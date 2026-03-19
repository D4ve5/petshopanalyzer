
# app.py — Pet Shop Analyzer (no matplotlib needed)

import streamlit as st
import pandas as pd
from io import StringIO

st.set_page_config(page_title='Pet Shop Analyzer', layout='wide')

st.title('🐶 Pet Shop Inventory & Expiry Analyzer')
st.markdown('Upload a CSV or paste data from Square or Excel.')

uploaded_file = st.file_uploader('Upload CSV', type=['csv', 'xlsx'], help='Columns: Date, Item Name, Quantity Sold, Gross Sales')

paste_data = st.text_area('Paste CSV text here (optional)')

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
elif paste_
    df = pd.read_csv(StringIO(paste_data))
else:
    st.info('Upload a CSV file or paste data to continue.')
    st.stop()

needed = ['Date', 'Item Name', 'Quantity Sold', 'Gross Sales']
if not all(c in df.columns for c in needed):
    st.error(f'Please include these columns: {", ".join(needed)}')
    st.dataframe(df.head())
    st.stop()

df['Date'] = pd.to_datetime(df['Date'])
df['Cost'] = df.get('Cost', 0)
df['Cost'] = pd.to_numeric(df['Cost'], errors='coerce').fillna(0)
df['Profit'] = df['Gross Sales'] - df['Cost']
df['Margin %'] = ((df['Profit'] / df['Gross Sales']) * 100).round(1)

df = df.rename(columns={'Item Name': 'Item'})

df['YearMonth'] = df['Date'].dt.to_period('M')
monthly = df.groupby(['YearMonth', 'Item']).agg({
    'Quantity Sold': 'sum',
    'Gross Sales': 'sum',
    'Profit': 'sum',
    'Margin %': 'mean'
}).round(2).reset_index()

# Summary
st.subheader('📊 Summary')
st.write(f"Total Revenue: £{df['Gross Sales'].sum():,.2f}")
st.write(f"Total Profit: £{df['Profit'].sum():,.2f}")
st.write(f"Average Margin: {df['Margin %'].mean():.1f}%")

st.subheader('📈 Top Items (Revenue)')
st.dataframe(monthly.nlargest(5, 'Gross Sales')[['Item', 'YearMonth', 'Gross Sales', 'Quantity Sold', 'Profit']])

# Simple line chart via Streamlit (no matplotlib)
st.subheader('📉 Revenue by Month')
st.line_chart(monthly.pivot(index='YearMonth', columns='Item', values='Gross Sales').fillna(0))

# Download CSV
def df_to_csv(df):
    import io
    return df.to_csv(index=False).encode('utf-8')

csv = df_to_csv(monthly)
st.download_button(
    label='💾 Download Report CSV',
    data=csv,
    file_name='petshop_analysis.csv',
    mime='text/csv'
)
