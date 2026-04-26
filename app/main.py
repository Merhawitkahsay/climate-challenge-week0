import streamlit as st
import matplotlib.pyplot as plt
from utils import load_data, filter_data, compute_summary

st.set_page_config(page_title="Climate Dashboard", layout="wide")

st.title("Climate Analysis Dashboard for COP32")
st.caption("Interactive tool for cross-country climate insights")

# Load data
@st.cache_data
def get_data():
    return load_data()

df = get_data()

# Sidebar filters
st.sidebar.header("Filter Options")

selected_countries = st.sidebar.multiselect(
    "Select Countries",
    df["Country"].unique(),
    default=df["Country"].unique()
)

year_range = st.sidebar.slider(
    "Select Year Range",
    int(df["Date"].dt.year.min()),
    int(df["Date"].dt.year.max()),
    (2015, 2026)
)

variable = st.sidebar.selectbox(
    "Select Variable",
    ["T2M", "PRECTOTCORR", "RH2M", "WS2M"]
)

# Filter data
filtered_df = filter_data(df, selected_countries, year_range)

# Time series plot
st.subheader("Time Series Analysis")

fig, ax = plt.subplots()

for country in selected_countries:
    temp = filtered_df[filtered_df["Country"] == country]
    monthly = temp.resample("ME", on="Date")[variable].mean()
    ax.plot(monthly.index, monthly.values, label=country)

ax.set_title(f"{variable} Trend Over Time")
ax.set_xlabel("Date")
ax.set_ylabel(variable)
ax.legend()

st.pyplot(fig)

# Summary stats
st.subheader("Summary Statistics")
summary = compute_summary(filtered_df, variable)
st.dataframe(summary)

# Distribution plot
st.subheader("Distribution Analysis")

fig2, ax2 = plt.subplots()

for country in selected_countries:
    temp = filtered_df[filtered_df["Country"] == country]
    ax2.hist(temp[variable].dropna(), bins=30, alpha=0.5, label=country)

ax2.set_title(f"{variable} Distribution")
ax2.legend()

st.pyplot(fig2)

# Insights
st.subheader("Key Insights")

st.markdown(
    """
    - Climate patterns vary significantly across countries  
    - Temperature and rainfall variability indicate increasing climate stress  
    - Extreme conditions highlight vulnerability differences  
    - Supports evidence-based decision-making for COP32  
    """
)