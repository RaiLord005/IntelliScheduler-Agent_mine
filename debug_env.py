import os
from dotenv import load_dotenv

print("--- DEBUGGING ENVIRONMENT VARIABLES ---")

# 1. Try to load the file
loaded = load_dotenv()
print(f"1. Did .env file load? -> {loaded}")

if not loaded:
    print("[ERROR] Python cannot find '.env'. Make sure it is in the same folder as this script!")
else:
    print("[SUCCESS] File found.")

# 2. Check the specific values
host = os.getenv('DB_HOST')
user = os.getenv('DB_USER')
pw = os.getenv('DB_PASSWORD')
db = os.getenv('DB_NAME')

print(f"2. DB_HOST:     {host}")
print(f"3. DB_USER:     {user}")
# We hide the password for safety, but check if it's None
print(f"4. DB_PASSWORD: {'(Set)' if pw else '[ERROR] MISSING (Is None)'}")
print(f"5. DB_NAME:     {db}")

print("---------------------------------------")

if not pw:
    print("[ERROR] CRITICAL: The password is missing. Check your .env file spelling!")
else:
    print("[SUCCESS] SUCCESS: Variables are loading. Restart your app."))