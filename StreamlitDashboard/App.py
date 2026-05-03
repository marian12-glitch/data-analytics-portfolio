import streamlit as st
import pandas as pd
import plotly.express as px
import os

#st.write("App is running!")
#st.write(os.getcwd())

st.title("Ames Housing Market Analysis")

st.markdown("An interactive dashboard exploring house prices in Ames, Iowa.")

df = pd.read_csv('house_prices_cleaned.csv')

st.write(f"Dataset contains **{df.shape[0]} houses** and **{df.shape[1]} features**")

# Sidebar filters
st.sidebar.header("Filters")

neighborhoods = ['All'] + sorted(df['Neighborhood'].unique().tolist())
selected_neighborhood = st.sidebar.selectbox("Select Neighborhood", neighborhoods)

# Filter dataframe based on selection
if selected_neighborhood == 'All':
    filtered_df = df
else:
    filtered_df = df[df['Neighborhood'] == selected_neighborhood]

st.write(f"Showing **{len(filtered_df)} houses**")

st.subheader("Price Distribution")

fig1 = px.histogram(
    filtered_df,
    x='SalePrice',
    nbins=50,
    title=f'Sale Price Distribution — {selected_neighborhood}',
    labels={'SalePrice': 'Sale Price ($)'},
    color_discrete_sequence=['#1F4E79']
)
st.plotly_chart(fig1, use_container_width=True)

# Price range slider
st.sidebar.subheader("Price Range")
min_price = int(df['SalePrice'].min())
max_price = int(df['SalePrice'].max())

price_range = st.sidebar.slider(
    "Select Price Range",
    min_value=min_price,
    max_value=max_price,
    value=(min_price, max_price)
)

# Apply price filter
filtered_df = filtered_df[
    (filtered_df['SalePrice'] >= price_range[0]) &
    (filtered_df['SalePrice'] <= price_range[1])
]

st.write(f"Showing **{len(filtered_df)} houses**")


# Two columns layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("Price by Neighbourhood")
    avg_price = filtered_df.groupby('Neighborhood')['SalePrice'].median().reset_index()
    avg_price = avg_price.sort_values('SalePrice', ascending=True)
    
    fig2 = px.bar(
        avg_price,
        x='SalePrice',
        y='Neighborhood',
        orientation='h',
        color='SalePrice',
        color_continuous_scale='Blues'
    )
    st.plotly_chart(fig2, use_container_width=True)

with col2:
    st.subheader("Living Area vs Price")
    fig3 = px.scatter(
        filtered_df,
        x='GrLivArea',
        y='SalePrice',
        color='OverallQual',
        color_continuous_scale='Blues',
        opacity=0.7
    )
    st.plotly_chart(fig3, use_container_width=True)


    # Correlation heatmap
st.subheader("Feature Correlations with Sale Price")

import plotly.graph_objects as go

numeric_df = filtered_df.select_dtypes(include=['int64', 'float64'])
corr = numeric_df.corr()
top_features = corr['SalePrice'].abs().sort_values(ascending=False).head(11).index
corr_top = corr.loc[top_features, top_features].round(2)

fig4 = go.Figure(data=go.Heatmap(
    z=corr_top.values,
    x=corr_top.columns,
    y=corr_top.columns,
    colorscale='Blues',
    text=corr_top.values,
    texttemplate='%{text}',
    zmin=-1,
    zmax=1
))
st.plotly_chart(fig4, use_container_width=True)

# Price trend over time
st.subheader("Price Trend Over Time")
price_by_year = filtered_df.groupby('YrSold')['SalePrice'].median().reset_index()

fig5 = px.line(
    price_by_year,
    x='YrSold',
    y='SalePrice',
    markers=True,
    color_discrete_sequence=['#1F4E79']
)
st.plotly_chart(fig5, use_container_width=True)