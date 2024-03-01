import psutil
import time
import mysql.connector
from datetime import datetime

# Function to collect system information
def get_system_info():
    cpu_percent = psutil.cpu_percent()
    memory_percent = psutil.virtual_memory().percent
    disk_percent = psutil.disk_usage('/').percent
    return cpu_percent, memory_percent, disk_percent

# Function to insert data into the database
def insert_data_into_db(cpu_percent, memory_percent, disk_percent):
    conn = mysql.connector.connect(
        host="localhost",
        port="3306",
        user="root",
        password="root",
        database="pchealthp"
    )
    cursor = conn.cursor()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("INSERT INTO system_stats (timestamp, cpu_percent, memory_percent, disk_percent) VALUES (%s, %s, %s, %s)",
            (timestamp, cpu_percent, memory_percent, disk_percent))
    conn.commit()
    conn.close()

# Main function
def main():
    while(1): 
        cpu_percent, memory_percent, disk_percent = get_system_info()
        insert_data_into_db(cpu_percent, memory_percent, disk_percent)
        print('data sent')
        time.sleep(5)

if __name__ == "__main__":
    main()