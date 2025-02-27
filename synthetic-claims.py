# python -m streamlit run synthetic-claims.py

import streamlit as st
import pandas as pd
import numpy as np
import string
import random

# Function to generate synthetic data
def generate_data(num_rows, columns):
    data = {}
    for col in columns:
        col_name = col['name']
        col_type = col['type']
        if col_type == 'int':
            data[col_name] = np.random.randint(col['min'], col['max'], num_rows)
        elif col_type == 'float':
            data[col_name] = np.random.uniform(col['min'], col['max'], num_rows)
        elif col_type == 'str':
            data[col_name] = [''.join(random.choices(string.ascii_letters + string.digits, k=col['length'])) for _ in range(num_rows)]
    return pd.DataFrame(data)

# Streamlit app
st.title('Synthetic Data Generator')

# User inputs
st.subheader('Data Size')
num_rows = st.number_input('Number of rows', min_value=1, value=10, max_value=100000)
num_cols = st.number_input('Number of columns', min_value=1, value=3,max_value=15)

st.subheader('Data Specification')
columns = []
for i in range(num_cols):
    col_name = st.text_input(f'Column {i+1} name')
    col1, col2, col3 = st.columns(3)
    with col1:
        col_type = st.selectbox(f'Column {i+1} type', ['int', 'float', 'str'])
    if col_type in ['int', 'float']:
        with col2:
            col_min = st.number_input(f'Column {i+1} min value', value=0)
        with col3:
            col_max = st.number_input(f'Column {i+1} max value', value=100)
        columns.append({'name': col_name, 'type': col_type, 'min': col_min, 'max': col_max})
    else:
        with col2:
            col_length = st.number_input(f'Column {i+1} string length', min_value=1, value=10)
        columns.append({'name': col_name, 'type': col_type, 'length': col_length})

if st.button('Generate Data'):
    df = generate_data(num_rows, columns)
    st.write(df)
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name='synthetic_data.csv',
        mime='text/csv',
    )