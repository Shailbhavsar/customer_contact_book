import mysql.connector

DB_CONFIG = {
    "host":"localhost",
    "user":"root",
    "password":"Admin1234",
    "database":"customer_book"
    }


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)
    
def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS states (
            id INT AUTO_INCREMENT PRIMARY KEY,
            state_name VARCHAR(100) NOT NULL UNIQUE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cities (
            id INT AUTO_INCREMENT PRIMARY KEY,
            city_name VARCHAR(100) NOT NULL,
            state_id INT NOT NULL,
            FOREIGN KEY (state_id) REFERENCES states(id),
            UNIQUE (city_name, state_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            phone VARCHAR(10) NOT NULL UNIQUE,
            email VARCHAR(255) NOT NULL UNIQUE,
            DOB DATE,
            Address VARCHAR(255) NOT NULL,
            city_id INT,
            FOREIGN KEY (city_id) REFERENCES cities(id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) NOT NULL UNIQUE,
            email VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            role VARCHAR(20) NOT NULL DEFAULT 'customer',
            customer_id INT,
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        )
    """)

    conn.commit()
    cursor.close()
    conn.close() 