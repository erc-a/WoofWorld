import psycopg2

try:
    # Connect to the database
    conn = psycopg2.connect(
        host="localhost",
        database="woofworld",
        user="ericadmin",
        password="ericadmin"
    )
    
    cur = conn.cursor()
    
    # Update the user role
    cur.execute(
        "UPDATE users SET role = 'admin' WHERE email = 'admin@test.com';"
    )
    
    # Check if any rows were affected
    if cur.rowcount > 0:
        print(f"Successfully updated {cur.rowcount} user(s) to admin role")
        
        # Verify the change
        cur.execute("SELECT id, name, email, role FROM users WHERE email = 'admin@test.com';")
        user = cur.fetchone()
        if user:
            print(f"User details: ID={user[0]}, Name={user[1]}, Email={user[2]}, Role={user[3]}")
    else:
        print("No user found with email admin@test.com")
    
    # Commit the changes
    conn.commit()
    
except Exception as e:
    print(f"Error: {e}")
    if 'conn' in locals():
        conn.rollback()
finally:
    if 'cur' in locals():
        cur.close()
    if 'conn' in locals():
        conn.close()
