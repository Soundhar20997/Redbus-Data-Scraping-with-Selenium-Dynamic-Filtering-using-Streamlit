
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Set up page configuration
st.set_page_config(page_title="Redbus Data Analysis", layout="wide")

# Load data
df = pd.read_csv("C:\Soundhar\Project\Redbus\Final_busdetails_df.csv")

# Ensure 'Seats_Available' column is numeric, replace non-numeric values with 0
df['Seats_available'] = pd.to_numeric(df['Seats_available'], errors='coerce').fillna(0)

# Ensure 'ticket_price' column is numeric, replace non-numeric values with 0
df['Price'] = pd.to_numeric(df['Price'], errors='coerce').fillna(0)

# Display app title and description
st.image("C:\Soundhar\VS Code\project\edbus.png",width=100)
st.title("Redbus Data Scraping & Analysis Dashboard")
st.markdown("""
    This app helps visualize and filter bus travel data scraped from Redbus. 
    Filter by various parameters and gain insights into schedules, prices, seat availability, and more!
""")

# Define the layout for filters and main display area
col1, col2, col3 = st.columns(3)

# Filter by route
routes = df['Route_name'].unique()
selected_route = col1.selectbox("Select Route", routes)

# Filter by bus type with "All Types" option
bus_types = df[df['Route_name'] == selected_route]['Bus_type'].unique()  # Get unique bus types for the selected route
bus_types = ["All Types"] + list(bus_types)  # Add "All Types" as the first option
selected_bus_type = col2.selectbox("Select Bus Type", bus_types)

# Filter by price range with step option
min_price = df['Price'].min()
max_price = df['Price'].max()
price_range = col3.slider("Price Range", min_price, max_price, (min_price, max_price), step=10.00)

# Filter by star rating (if column exists in the DataFrame)
if 'Ratings' in df.columns:
    min_rating = df['Ratings'].min()
    max_rating = df['Ratings'].max()
    rating = st.slider("Select Minimum Star Rating", min_value=min_rating, max_value=max_rating, step=0.5, value=min_rating)
    st.write(f"Filtering buses with at least {rating} ⭐ rating.")
else:
    st.warning("Star rating column not found in the dataset.")

# Apply all filters
if selected_bus_type == "All Types":
    filtered_df = df[
        (df['Route_name'] == selected_route) &
        (df['Price'] >= price_range[0]) &
        (df['Price'] <= price_range[1]) &
        (df['Ratings'] >= rating if 'Ratings' in df.columns else True)
    ]
else:
    filtered_df = df[
        (df['Route_name'] == selected_route) &
        (df['Bus_type'] == selected_bus_type) &
        (df['Price'] >= price_range[0]) &
        (df['Price'] <= price_range[1]) &
        (df['Ratings'] >= rating if 'Ratings' in df.columns else True)
    ]

# Display KPIs based on the filtered DataFrame
st.markdown("### Key Metrics for Selected Route and Bus Type")
kpi1, kpi2, kpi3 = st.columns(3)

average_price = filtered_df['Price'].mean() if not filtered_df.empty else 0
total_seats = int(filtered_df['Seats_available'].sum()) if not filtered_df.empty else 0
bus_count = filtered_df['Bus_name'].nunique() if not filtered_df.empty else 0

kpi1.metric(label="Average Price", value=f"Rs. {average_price:.2f}")
kpi2.metric(label="Total Seats Available", value=total_seats)
kpi3.metric(label="Total Bus Available", value=bus_count)

# Display filtered data
st.markdown("### Filtered Bus Data")
if not filtered_df.empty:
    st.dataframe(filtered_df)
else:
    st.warning("No buses found for the selected criteria.")

# Visualizations
st.markdown("### Price Distribution")
if not filtered_df.empty:
    fig, ax = plt.subplots()
    sns.histplot(filtered_df['Price'], bins=20, kde=True, color='blue', ax=ax)
    ax.set_xlabel("Price")
    ax.set_ylabel("Frequency")
    st.pyplot(fig)

    if 'Seats_Available' in filtered_df.columns:
        st.markdown("### Price vs. Seats Available")
        fig2, ax2 = plt.subplots()
        sns.scatterplot(x='Price', y='Seats_available', data=filtered_df, ax=ax2)
        ax2.set_xlabel("Ticket Price")
        ax2.set_ylabel("Seats Available")
        st.pyplot(fig2)

# Custom CSS for Styling
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
        color: #333;
    }
    .stButton>button {
        color: white;
        background: #007bff;
    }
    .stMetric {
        background-color: #f8f9fa;
        border: 1px solid #ddd;
        padding: 10px;
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)
