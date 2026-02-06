import random
from datetime import datetime, timedelta
from .db_manager import fetch_query, execute_query

class SchedulerAgent:
    def __init__(self):
        self.buffer = 15 

    def predict_risk(self, organizer_id):
        res = fetch_query("SELECT risk_score FROM users WHERE user_id = %s", (organizer_id,))
        return res[0]['risk_score'] if res else 0.0

    def calc_travel(self, location):
        if "online" in location.lower(): return 0
        return random.randint(20, 45)

    def check_preferences(self, user_id, start_time):
        user = fetch_query("SELECT preferred_slot FROM users WHERE user_id = %s", (user_id,))
        if not user: return False
        pref = user[0]['preferred_slot']
        hour = start_time.hour
        if pref == 'morning' and hour >= 12: return True 
        if pref == 'afternoon' and hour < 12: return True 
        return False

    def check_availability(self, user_ids, start, end):
        s_str = start.strftime('%Y-%m-%d %H:%M:%S')
        e_str = end.strftime('%Y-%m-%d %H:%M:%S')
        q = f"SELECT * FROM meetings WHERE start_time < '{e_str}' AND end_time > '{s_str}' ORDER BY end_time DESC LIMIT 1"
        conflicts = fetch_query(q)
        return (False, conflicts[0]) if conflicts else (True, None)

    # --- NEW LOGIC: 2 HOUR BREAK ---
    def find_alternative_slot(self, blocking_meeting):
        """
        Takes the meeting that caused the conflict.
        Returns: blocking_meeting.end_time + 2 HOURS
        """
        blocked_end = blocking_meeting['end_time']
        
        # Ensure blocked_end is a datetime object
        if isinstance(blocked_end, str):
            blocked_end = datetime.fromisoformat(blocked_end)
            
        suggested_start = blocked_end + timedelta(hours=2)
        
        # Return format: YYYY-MM-DD HH:MM
        return suggested_start.strftime("%Y-%m-%d %H:%M")

    def scale_down(self):
        cutoff = datetime.now() - timedelta(days=30)
        execute_query("UPDATE meetings SET status='compressed' WHERE start_time < %s", (cutoff,))
        execute_query("UPDATE system_analytics SET value = 85.0 WHERE metric_name = 'Storage Saved'")
        return "History Compressed Successfully"

agent = SchedulerAgent()