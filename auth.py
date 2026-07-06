import datetime
import os

import bcrypt
import jwt

import validation
import customers
import database

JWT_SECRET = os.environ.get("JWT_SECRET")
if not JWT_SECRET:
    raise RuntimeError("JWT_SECRET environment variable is not set.")

JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_MINUTES = 60

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_jwt_token(username,expiration_minutes=JWT_EXPIRATION_MINUTES):
    now = datetime.datetime.now(datetime.timezone.utc)
    payload = {
        "sub": username,
        "iat": now,
        "exp": now + datetime.timedelta(minutes=expiration_minutes)
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    if isinstance(token, bytes):
        token = token.decode('utf-8')  
    return token

def decode_jwt_token(token):
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        print("Token has expired.")
    except jwt.InvalidTokenError:
        print("Invalid token.")
        return None
    
    
def link_or_create_user(username,email):
    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM customers WHERE  email = %s", (email,))
    existing = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if existing:
        customer_id = existing[0]
        print(f"customer with email {email} already exists.")
    else:
        print("no existing user found, creating new user...")
        add_now = input("Do you want to create a new user? (y/n): ").strip().lower()
        if add_now != 'y':
            print ("skipping user creation.")
            return 
        customer_id = customers.add_customer(email=email)
        
    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET customer_id = %s WHERE username = %s", (customer_id, username)
    )
    
    conn.commit()
    cursor.close()
    conn.close()
    print("Account linked successfully.")
    
    
def signup():
    print("\n--- Sign Up ---")
    
    while True:
        username = input("Enter a username: ").strip()
        if not validation.validate_username(username):
            print("Invalid username. Please try again.")
            continue
        
        conn = database.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        exists = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if exists:
            print("Username already exists. Please choose a different username.")
            continue
        break
    
    while True:
        email = input("Enter your email: ").strip()
        if not validation.is_valid_email_format(email):
            continue
        
        conn = database.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        exists = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if exists:
            print("Email already exists. Please choose a different email.")
            continue
        break
    
    while True:
        password = input("Enter a password: ").strip()
        if  validation.validate_password(password):
            break
        
    while True:
        confirm = input("Confirm your password: ").strip()
        if confirm == password:
            break
        print("Passwords do not match. Please try again.")

    hashed_password = hash_password(password)
    
    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, hashed_password))
    
    conn.commit()
    cursor.close()
    conn.close()
    print("Account created successfully.")
    
    link_or_create_user(username,email)
    
    
def login():
    print("\n--- Login ---")
    
    for attempt in range(3):
        username = input("Enter your username: ").strip()
        password = input("Enter your password: ").strip()
        
        conn = database.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if user and verify_password(password, user[0]):
            token = create_jwt_token(username)
            print("Login successful.")
            print(f"Your JWT token: {token}")
            return token
        else:
            remaining_attempts = 2 - attempt
            if remaining_attempts > 0:
                print(f"Invalid username or password. You have {remaining_attempts} attempts left.")
            else:
                print("too many failed attemts. Please try again later.")
                return None
    return None

