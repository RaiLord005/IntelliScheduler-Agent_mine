from scripts.db_manager import execute_query, fetch_query

print("--- DIAGNOSTIC START ---")

# 1. Test Users Table
print("\n1. Checking Users Table...")
users = fetch_query("SELECT * FROM users")
if users:
    print(f"[SUCCESS] Found {len(users)} users.")
    print(f"   First User: {users[0]['username']} (ID: {users[0]['user_id']})")
else:
    print("[WARNING] Users table is empty or connection failed.")
    # Try to insert a test user
    print("   Attempting to create Test User...")
    execute_query("INSERT INTO users (username, password) VALUES ('SystemTestUser', '1234')")

# 2. Test Meetings Table
print("\n2. Checking Meetings Table Structure...")
try:
    # Try a dummy insert to see if columns exist
    success = execute_query("""
        INSERT INTO meetings (title, organizer_id, participant_id, start_time, end_time, location)
        VALUES ('TEST MEETING', 1, 1, '2025-01-01 10:00:00', '2025-01-01 11:00:00', 'TestLoc')
    """)
    if success:
        print("[SUCCESS] Inserted test meeting.")
        print("[SUCCESS] The 'participant_id' column exists and works.")
    else:
        print("[ERROR] FAILED: Could not insert meeting.")
        print("   This likely means your Database Schema is outdated.")
except Exception as e:
    print(f"[ERROR] CRITICAL ERROR: {e}")

print("\n--- DIAGNOSTIC END ---")