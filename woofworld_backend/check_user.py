import psycopg2

try:
    print("Connecting to database...")
    conn = psycopg2.connect(host='localhost', database='woofworld', user='ericadmin', password='ericadmin')
    print("Connected successfully")
    
    cur = conn.cursor()
    cur.execute("SELECT id, name, email, role FROM users WHERE email='admin@test.com';")
    result = cur.fetchone()
    print(f"User in database: {result}")
    
    # Also check all users
    cur.execute("SELECT id, name, email, role FROM users;")
    all_users = cur.fetchall()
    print(f"All users: {all_users}")
    
    cur.close()
    conn.close()
    print("Connection closed")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
