# python -m streamlit run synthetic-claims.py

import streamlit as st
import pandas as pd
import numpy as np
import string
import random
import datetime


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
        elif col_type == 'date':
            start_date = pd.to_datetime(col['min'])
            end_date = pd.to_datetime(col['max'])
            data[col_name] = start_date + (end_date - start_date) * np.random.rand(num_rows)
            data[col_name] = pd.Series(data[col_name])
            data[col_name] = data[col_name].dt.strftime('%Y-%m-%d')
        elif col_type == 'category':
            cat_list = col['cats'].split(',')
            data[col_name] = [random.choice(cat_list) for _ in range(num_rows)]
    return pd.DataFrame(data)

# Streamlit app
st.sidebar.title('Synthetic Data Generator')
st.sidebar.write("Random data generator. Creates a table of data of common field types that can be configured and downloaded as a CSV")
st.sidebar.write("Enter size of dataset to generate. Limit 100,000 rows and 15 columns")

# User inputs
st.sidebar.subheader('Data Size')
num_rows = st.sidebar.number_input('Number of rows', min_value=1, value=10, max_value=100000)
num_cols = st.sidebar.number_input('Number of columns', min_value=1, value=3,max_value=18)

st.subheader('Data Specification')
st.write('Specify the solumn names, values and relevant parameters as per below and click generate to get a lovely slug of random data.')
columns = []
for i in range(num_cols):
    st.divider()
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        col_name = st.text_input(f'Column {i+1} name', key=f'col_name_{i}')
    with col2:
        col_type = st.selectbox(f'Column {i+1} type', ['int', 'float', 'str','date','category'])
    if col_type in ['int', 'float']:
        with col3:
            col_min = st.number_input(f'Column {i+1} min value', value=0)
        with col4:
            col_max = st.number_input(f'Column {i+1} max value', value=100)
        columns.append({'name': col_name, 'type': col_type, 'min': col_min, 'max': col_max})
    else:
        if col_type == 'str':
            with col3:
                col_length = st.number_input(f'Column {i+1} string length', min_value=1, value=10, key=f'str_name_{i}')
            columns.append({'name': col_name, 'type': col_type, 'length': col_length})  
        elif col_type == 'category':
            with col3:
                col_cats = st.text_area(f'Enter comma seperated category values:', key=f'cat_name_{i}')
            columns.append({'name': col_name, 'type': col_type, 'cats': col_cats})
        else:
            with col3:
                max_date = st.date_input("Max Date", datetime.date(2025, 1, 1), key=f'max_date_name_{i}')
            with col4:
                min_date = st.date_input("Min Date", datetime.date(2024, 1, 1), key=f'min_date_name_{i}')
            columns.append({'name': col_name, 'type': col_type, 'min': min_date, 'max': max_date})

if st.button('Generate Data'):
    df = generate_data(num_rows, columns)
    df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x) # remove leading/trailing spaces from category labels
    df = df.apply(lambda x: round(x, 2) if x.dtype == 'float' else x) # round any float columns to 2 decimal places


    st.write(df)
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name='synthetic_data.csv',
        mime='text/csv',
    )
