# shared/database.py
import mysql.connector
from mysql.connector import Error
import hashlib

# --- IMPORTANT ---
# UPDATE THIS WITH YOUR MYSQL DATABASE CREDENTIALS
# You must create the 'pup_shop' database manually first.
# Example: CREATE DATABASE pup_shop;
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Test1234!', # <-- CHANGE THIS
    'database': 'pup_shop'
}

def get_db_connection():
    """Establishes a connection to the database."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            return conn
    except Error as e:
        print(f"Error connecting to MySQL database: {e}")
        return None

def hash_password(password):
    """Hashes a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def init_db():
    """Initializes the database, creating tables and inserting sample data if they don't exist."""
    conn = get_db_connection()
    if not conn:
        print("Could not connect to DB for initialization.")
        return
    cursor = conn.cursor()

    try:
        # Create Tables
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE,
            password_hash VARCHAR(255) NOT NULL,
            address1 TEXT,
            address2 TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            description TEXT,
            price DECIMAL(10, 2) NOT NULL,
            stock INT NOT NULL,
            image_url VARCHAR(255),
            sold_count INT DEFAULT 0
        )
        """)
        
        # Check if products table is empty before inserting
        cursor.execute("SELECT COUNT(*) FROM products")
        if cursor.fetchone()[0] == 0:
            print("Populating sample products...")
            sample_products = [
                ('PUP Minimalist Baybayin Lanyard', 'Coquette Style Baybayin Lanyard', 140.00, 100, '/static/images/product_lanyard.png', 50),
                ('PUP Jeepney Signage', 'Collectible Iskolar Script Signage', 20.00, 200, '/static/images/product_jeepney.png', 112),
                ('PUP Iskolar TOTE BAG (White)', 'White Tote Bag with Iskolar Script', 160.00, 75, '/static/images/product_tote1.png', 45),
                ('PUP Iskolar TOTE BAG (Black)', 'Black Tote Bag with Iskolar Script', 160.00, 75, '/static/images/product_tote2.png', 30),
                ('PUP STUDY WITH STYLE Shirt', 'PUP Obelisk silhouette design shirt', 450.00, 50, '/static/images/product_shirt.png', 88),
            ]
            cursor.executemany(
                "INSERT INTO products (name, description, price, stock, image_url, sold_count) VALUES (%s, %s, %s, %s, %s, %s)",
                sample_products
            )

        conn.commit()
        print("Database initialized successfully.")
    except Error as e:
        print(f"Error during DB initialization: {e}")
    finally:
        cursor.close()
        conn.close()

# --- Product CRUD Functions ---
def get_all_products():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products ORDER BY id DESC")
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return products

def add_product(name, quantity, price):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO products (name, stock, price, description, image_url) VALUES (%s, %s, %s, %s, %s)",
            (name, quantity, price, 'Added from admin panel', '/static/images/pup_logo.png')
        )
        conn.commit()
        return True
    except Error as e:
        print(f"Error adding product: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def update_product(item_id, name, quantity, price):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE products SET name=%s, stock=%s, price=%s WHERE id=%s",
            (name, quantity, price, item_id)
        )
        conn.commit()
        return True
    except Error as e:
        print(f"Error updating product: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def delete_product(item_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM products WHERE id=%s", (item_id,))
        conn.commit()
        return True
    except Error as e:
        print(f"Error deleting product: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

# Run this once to setup the DB
if __name__ == '__main__':
    print("Running DB Initializer...")
    init_db()