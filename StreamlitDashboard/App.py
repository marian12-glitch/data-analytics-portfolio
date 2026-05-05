import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(page_title="Ames Housing Market", page_icon="🏠", layout="wide")

st.title("🏠 Ames Housing Market Analysis")
st.markdown("An interactive dashboard exploring house prices in Ames, Iowa.")

df = pd.read_csv(os.path.join(os.path.dirname(__file__), 'house_prices_cleaned.csv'))
st.write(f"Dataset contains **{df.shape[0]} houses** and **{df.shape[1]} features**")

# Sidebar filters
st.sidebar.header("Filters")

neighborhoods = ['All'] + sorted(df['Neighborhood'].unique().tolist())
selected_neighborhood = st.sidebar.selectbox("Select Neighborhood", neighborhoods)

st.sidebar.subheader("Price Range")
min_price = int(df['SalePrice'].min())
max_price = int(df['SalePrice'].max())
price_range = st.sidebar.slider(
    "Select Price Range",
    min_value=min_price,
    max_value=max_price,
    value=(min_price, max_price)
)

# Apply filters
if selected_neighborhood == 'All':
    filtered_df = df
else:
    filtered_df = df[df['Neighborhood'] == selected_neighborhood]

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

# Key Insights
st.subheader("📊 Key Business Insights")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Most Expensive Neighbourhood", "NridgHt", "$315,000 median")

with col2:
    st.metric("Least Expensive Neighbourhood", "MeadowV", "$88,000 median")

with col3:
    st.metric("Price Difference", "$227,000", "between best and worst")

st.markdown("""
**Key Findings:**
- Overall quality is the strongest predictor of sale price (correlation: 0.79)
- Neighbourhood alone can account for over 227k difference in price
- Newer houses command higher prices — negative correlation with age
- House prices peaked in 2007 before declining due to the 2008 financial crisis
""")
