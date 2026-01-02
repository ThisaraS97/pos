#!/usr/bin/env python
import sys
sys.path.insert(0, 'backend')
from passlib.context import CryptContext
import sqlite3

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Test password hashing and verification
test_password = "admin123"
hashed = pwd_context.hash(test_password)
print(f"Original password: {test_password}")
print(f"Hashed: {hashed[:50]}...")

# Test verification
is_correct = pwd_context.verify(test_password, hashed)
print(f"Verification result: {is_correct}")

# Now test with database hash
conn = sqlite3.connect('anypos.db')
cursor = conn.cursor()
cursor.execute('SELECT hashed_password FROM users WHERE username = "admin" LIMIT 1')
result = cursor.fetchone()
if result:
    db_hash = result[0]
    conn.close()
    
    print(f"\nDatabase hash: {db_hash[:50]}...")
    is_db_correct = pwd_context.verify(test_password, db_hash)
    print(f"DB verification result: {is_db_correct}")
else:
    print("Admin user not found!")
