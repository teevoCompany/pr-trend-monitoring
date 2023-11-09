import streamlit as st
from pytrends.request import TrendReq
from pytrends import dailydata
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import base64
import time  # Import the time module

# Create a Streamlit app with multiple pages using the "st" session state
def main():
    st.title("Streamlit Multi-Page App")
    
    menu = ["Search Volume Visualization", "Related Queries"]
    choice = st.sidebar.selectbox("Select a Page", menu)
    
    if choice == "Search Volume Visualization":
        search_volume_page()
    elif choice == "Related Queries":
        related_queries_page()

# Page 1: Search Volume Visualization
def search_volume_page():
    st.title("Search Volume Visualization")
    st.write("Customize the search term, date range, and additional features below:")
    # ... (Your original code for search volume visualization)

    # User input for keyword
    keyword = st.text_input("Enter a search keyword:", "Prabowo Gibran")

    # User input for date range
    start_date = st.date_input("Start Date", pd.to_datetime("2023-10-01"))
    end_date = st.date_input("End Date", pd.to_datetime("2023-11-30"))

    # Additional features
    show_moving_average = st.checkbox("Show Moving Average")
    dynamic_y_axis = st.checkbox("Dynamic Y-Axis Scaling")

    # Convert user input date to year and month
    start_year = start_date.year
    start_month = start_date.month
    stop_year = end_date.year
    stop_month = end_date.month

    # Specify the geo location
    geo = 'ID'  # Geo code for Indonesia

    # Fetch daily data for the specified keyword and date range
    df = dailydata.get_daily_data(keyword, start_year, start_month, stop_year, stop_month, geo=geo)

    # Display the data in a Streamlit DataFrame widget
    st.write("Search Volume Data:")
    st.write(df)

    # Set the figure size
    fig, ax = plt.subplots(figsize=(12, 6))

    # Plot the daily search volume data
    sns.lineplot(data=df, x=df.index, y=keyword, label="Search Volume", ax=ax)

    # Show moving average if selected
    if show_moving_average:
        df[f'{keyword}_MA'] = df[keyword].rolling(window=7).mean()
        sns.lineplot(data=df, x=df.index, y=f'{keyword}_MA', label="Moving Average", ax=ax)

    # Set labels and title
    ax.set_xlabel("Date")
    ax.set_ylabel("Search Volume")

    # Set Y-axis scaling
    if dynamic_y_axis:
        ax.set_ylim(0, df[keyword].max())

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)

    # Show the plot using Streamlit's 'st.pyplot' function
    st.pyplot(fig)

    # Add a description
    st.write(f"This chart shows the daily search volume for '{keyword}' in Indonesia from {start_date} to {end_date}.")

    # Calculate and display basic statistics
    st.write("Basic Statistics:")
    st.write(f"Mean Search Volume: {df[keyword].mean()}")
    st.write(f"Median Search Volume: {df[keyword].median()}")
    st.write(f"Maximum Search Volume: {df[keyword].max()}")
    st.write(f"Minimum Search Volume: {df[keyword].min()}")


# Page 2: Related Queries
def related_queries_page():
    st.title("Related Queries")
    st.write("Customize the search term, date range, and additional features below:")

    # User input for keyword
    keyword = st.text_input("Enter a search keyword:", "Prabowo Gibran")

    # User input for date range
    start_date = st.date_input("Start Date", pd.to_datetime("2023-10-01"))
    end_date = st.date_input("End Date", pd.to_datetime("2023-11-30"))

    # Retrieve related queries using Google Trends
    pytrend = TrendReq()
    kw_list = [keyword]
    pytrend.build_payload(kw_list=kw_list)
    related_queries = pytrend.related_queries()
    related_query_data = related_queries.get(keyword, pd.DataFrame())

    # Display related queries separately
    if 'top' in related_query_data:
        st.write("Top Related Queries:")
        st.dataframe(related_query_data['top'])

    if 'rising' in related_query_data:
        st.write("Rising Related Queries:")
        st.dataframe(related_query_data['rising'])

    # Continue with your existing code to fetch and display search volume data and visualize it as you did before.
    # ...

    # Plot the bar graph for top related queries if available
    if 'top' in related_query_data:
        top_related_queries = related_query_data['top']
        plt.figure(figsize=(15, 8))
        plt.bar(top_related_queries["query"], top_related_queries["value"])
        plt.xlabel("Top Queries")
        plt.ylabel("Top Query Value")
        plt.title("Top Queries and their values")
        plt.xticks(rotation=90)
        st.pyplot(plt)

    # Add a description
    st.write(f"This chart shows the daily search volume for '{keyword}' in Indonesia from {start_date} to {end_date}.")


# Function to generate download link
def download_link(object_to_download, download_filename, download_link_text):
    if isinstance(object_to_download, plt.Figure):
        object_to_download.savefig(download_filename)
    b64 = base64.b64encode(open(download_filename, 'rb').read()).decode()
    return f'<a href="data:file/png;base64,{b64}" download="{download_filename}">{download_link_text}</a>'

if __name__ == "__main__":
    main()
