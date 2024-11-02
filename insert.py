import sqlite3
from datetime import datetime

DOTNET_EPOCH = datetime(1, 1, 1)

def convert_to_dotnet_ticks(dt):
    # Convert a datetime object to .NET ticks in case you need it
    ticks = (dt - DOTNET_EPOCH).total_seconds() * 10**7
    return int(ticks)
    
def display_descriptions(cursor):
    # Display all records from the DESCRIPTION table and ask the user to select one.
    cursor.execute("SELECT * FROM DESCRIPTION;")
    columns = cursor.fetchall()

    for columns_info in columns:
        print(columns_info)

    # Prompt user for the description_id
    print("The description_id flag need to correspond with the product AND the data format in your file e.g: ticks/1 minutes etc...")
    description_id = int(input("Enter the number corresponding to the description_id you want to use: "))

    return description_id
    
def insert_line_into_last_table(cursor, line, description_id):
    # Parse a single line of data and insert it directly into the LAST table.
    # Strip whitespace and skip empty lines
    line = line.strip()
    if not line:
        return

    # You may need to adapt this
    # Split the line by semicolon and convert to appropriate types
    values = line.split(";")
    price = float(values[0])
    # In case you need to covnert to dotnet tick time use and adapt this as you need
    # dt = datetime.strptime(date_part + time_part, "%Y%m%d%H%M%S")
    # time = convert_to_dotnet_ticks(dt)
    time = int(values[2])
    volume = float(values[3])
    aggressor = int(values[4])
    tick_direction = int(values[5])
    open_interest = float(values[6])
    buyer = values[7] if values[7] != 'None' else None
    seller = values[8] if values[8] != 'None' else None
    funding_rates = float(values[9]) if values[9] != 'None' else 0.0
    quote_asset_volume = values[10] if values[10] != 'None' else None

    # Insert data into the LAST table
    cursor.execute('''
        INSERT INTO LAST (price, description_id, time, volume, aggressor, tick_direction, open_interest, 
                          buyer, seller, funding_rates, quote_asset_volume) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    ''', (price, description_id, time, volume, aggressor, tick_direction, open_interest, 
          buyer, seller, funding_rates, quote_asset_volume))

def process_file_and_insert_into_db(database_name):
    # Connect to the SQLite database
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
    
    description_id = display_descriptions(cursor)
    print("You need to have time set to UTC timzone and in dotnet tick format !\n")
    filename = input("Enter the name of the file to import: ")
    
    # Process the file and insert each line into the database
    with open(filename, 'r') as file:
        for line in file:
            insert_line_into_last_table(cursor, line, description_id)
    
    # Commit the transaction and close the connection
    conn.commit()
    conn.close()
    print("Data inserted successfully.")

# You need to change this
database_name = "C:\\Users\\Path\\To\\Quantower\\AMP Quantower\\History\\AMP47CQG\\history.db"

# Process and insert data into the database
process_file_and_insert_into_db(database_name)
