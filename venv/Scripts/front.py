import streamlit as st
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
import sqlalchemy
from datetime import datetime, timedelta

# Function to fetch data from the database
def fetch_data_from_db():
    engine = sqlalchemy.create_engine("mysql+mysqlconnector://root:root@localhost:3306/pchealthp")
    with engine.connect() as conn:
        df = pd.read_sql_query("SELECT * FROM system_stats", conn)
    return df

# Function to format timestamp to desired string format
def format_timestamp(timestamp):
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

# Main function
def main():
    st.title("Health Tracker")

    # Fetch data from the database
    df = fetch_data_from_db()

    # Get the time range from the data
    min_timestamp = df['timestamp'].min()
    max_timestamp = df['timestamp'].max()

    # Convert min and max timestamps to midnight and 23:59:59
    min_time = min_timestamp.replace(hour=0, minute=0, second=0)
    max_time = max_timestamp.replace(hour=23, minute=59, second=59)

    # Add a range slider for time in the sidebar
    start_time, end_time = st.sidebar.slider("Select Time Range",
                                            min_value=min_time.timestamp(),
                                            max_value=max_time.timestamp(),
                                            value=[min_timestamp.timestamp(), max_timestamp.timestamp()],
                                            key="time_range_slider",
                                            format="YYYY-MM-DD HH:mm:ss"  # Use the desired format
                                            )

    # Convert start and end times back to datetime objects
    start_time_dt = datetime.utcfromtimestamp(start_time).replace(microsecond=0)
    end_time_dt = datetime.utcfromtimestamp(end_time).replace(microsecond=0)

    # Update the slider label to show the actual bounds
    st.sidebar.write(f"Selected Time Range: {start_time_dt.strftime('%Y-%m-%d %H:%M:%S')} to {end_time_dt.strftime('%Y-%m-%d %H:%M:%S')}")

    # Create checkboxes for selecting which graphs to display (checked by default)
    display_cpu = st.sidebar.checkbox("Display CPU Percent", value=True)
    display_memory = st.sidebar.checkbox("Display Memory Percent", value=True)
    display_disk = st.sidebar.checkbox("Display Disk Percent", value=True)

    # Filter data based on selected time range
    filtered_df = df[(df['timestamp'] >= start_time_dt) & (df['timestamp'] <= end_time_dt)]

    # Plot selected graphs based on checkboxes with a smooth curve
    if display_cpu:
        plt.figure(figsize=(10, 6))
        plt.plot(filtered_df['timestamp'], filtered_df['cpu_percent'], linestyle='-')
        plt.xlabel('Timestamp')
        plt.ylabel('CPU Percent')
        plt.title('CPU Percent Over Time')
        st.pyplot(plt)

    if display_memory:
        plt.figure(figsize=(10, 6))
        plt.plot(filtered_df['timestamp'], filtered_df['memory_percent'], linestyle='-')
        plt.xlabel('Timestamp')
        plt.ylabel('Memory Percent')
        plt.title('Memory Percent Over Time')
        st.pyplot(plt)

    if display_disk:
        plt.figure(figsize=(10, 6))
        plt.plot(filtered_df['timestamp'], filtered_df['disk_percent'], linestyle='-')
        plt.xlabel('Timestamp')
        plt.ylabel('Disk Percent')
        plt.title('Disk Percent Over Time')
        st.pyplot(plt)

    # Display system information on the right
    st.sidebar.subheader("System Information")
    st.sidebar.write(df)

if __name__ == "__main__":
    main()
