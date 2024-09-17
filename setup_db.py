import mysql.connector
from mysql.connector import Error

def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Vanathi@2003',
            database='retail_store'
        )
        return connection
    except Error as e:
        print(f"Error: {e}")
    return connection

def create_tables(connection):
    cursor = connection.cursor()
    connection.commit()

def insert_sample_data(connection):
    cursor = connection.cursor()
    
    inventory_data = [
        ('shoes', '9', 10),
        ('shoes', '8', 5),
        ('jacket', '8', 3),
        ('jacket', '10', 0),
        ('smartphone', 'N/A', 50)
    ]
    
    promotions_data = [
        ('smartphones', '10% off', '2024-12-31'),
        ('shoes', '15% off', '2024-09-30'),
        ('jackets', '5% off', '2024-10-15')
    ]
    
    cursor.executemany('INSERT INTO inventory (product, size, quantity) VALUES (%s, %s, %s)', inventory_data)
    cursor.executemany('INSERT INTO promotions (product_category, discount, valid_until) VALUES (%s, %s, %s)', promotions_data)
    
    connection.commit()

def main():
    connection = create_connection()
    if connection is not None:
        create_tables(connection)
        insert_sample_data(connection)
        connection.close()

if __name__ == "__main__":
    main()
