import sys
# FORCE WINDOWS TO ACCEPT SPECIAL CHARACTERS
sys.stdout.reconfigure(encoding='utf-8')

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from scripts.db_manager import fetch_query, execute_query
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from pathlib import Path
import traceback

# FORCE LOAD .ENV
base_dir = Path(__file__).resolve().parent
load_dotenv(base_dir / '.env')

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'FALLBACK_KEY_IF_MISSING')

# ==========================================
# 1. AUTHENTICATION
# ==========================================

@app.route('/')
def root(): return redirect(url_for('menu')) if 'user_id' in session else redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = fetch_query("SELECT * FROM users WHERE username = %s AND password = %s", 
                          (request.form['username'], request.form['password']))
        if user:
            session['user_id'] = user[0]['user_id']
            session['username'] = user[0]['username']
            return redirect(url_for('menu'))
        return render_template('login.html', error="Invalid Credentials")
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        if len(request.form['password']) < 6: return render_template('signup.html', error="Password too short")
        org = request.form.get('organization') or 'Freelancer'
        if execute_query("INSERT INTO users (username, password, organization) VALUES (%s, %s, %s)", (request.form['username'], request.form['password'], org)):
            return redirect(url_for('login'))
        return render_template('signup.html', error="Username Taken")
    return render_template('signup.html')

@app.route('/logout')
def logout(): session.clear(); return redirect(url_for('login'))

# ==========================================
# 2. PAGES
# ==========================================

@app.route('/menu')
def menu(): 
    if 'user_id' not in session: return redirect(url_for('login'))
    return render_template('menu.html', username=session['username'])

@app.route('/create_mode')
def create_mode():
    if 'user_id' not in session: return redirect(url_for('login'))
    
    # Get Data
    all_users = fetch_query("SELECT user_id, username, organization FROM users WHERE user_id != %s ORDER BY username", (session['user_id'],))
    orgs = fetch_query("SELECT DISTINCT organization FROM users WHERE user_id != %s AND organization != 'Freelancer' ORDER BY organization", (session['user_id'],))
    
    # Get Meetings (Crucial: Select invite_type)
    my_meetings = fetch_query("""
        SELECT m.*, u.username as participant_name, u.organization as participant_org
        FROM meetings m 
        JOIN users u ON m.participant_id = u.user_id 
        WHERE m.organizer_id = %s AND m.status != 'cancelled'
        ORDER BY m.start_time DESC
    """, (session['user_id'],))
    
    return render_template('create_meeting.html', 
                           username=session['username'], 
                           all_users=all_users, 
                           all_orgs=orgs, 
                           meetings=my_meetings)

@app.route('/join_mode')
def join_mode():
    if 'user_id' not in session: return redirect(url_for('login'))
    
    # Get Meetings for Lobby (Crucial: Select invite_type)
    meetings = fetch_query("""
        SELECT m.*, u.username as organizer_name
        FROM meetings m 
        JOIN users u ON m.organizer_id = u.user_id 
        WHERE (m.participant_id = %s OR m.organizer_id = %s) 
        AND m.status != 'cancelled'
        ORDER BY m.start_time ASC
    """, (session['user_id'], session['user_id']))
    
    return render_template('join_meeting.html', username=session['username'], meetings=meetings, my_id=session['user_id'])

# ==========================================
# 3. API ENDPOINTS
# ==========================================

@app.route('/api/refresh_analytics', methods=['POST'])
def refresh_analytics():
    try:
        user_res = fetch_query("SELECT COUNT(*) as c FROM users")
        mtg_res = fetch_query("SELECT COUNT(*) as c FROM meetings WHERE status != 'cancelled'")
        
        user_count = user_res[0]['c'] if user_res else 0
        mtg_count = mtg_res[0]['c'] if mtg_res else 0
        
        return jsonify({
            "status": "success",
            "metrics": {
                "compression": f"{min(95, 20 + (mtg_count * 2))}%",
                "overhead": f"{min(90, 15 + (mtg_count * 3))}%",
                "users": f"{user_count} Users",
                "time_saved": f"{mtg_count * 0.5} Hrs"
            }
        })
    except Exception as e: return jsonify({"status": "error", "message": str(e)})

@app.route('/api/get_slots', methods=['POST'])
def get_slots():
    try:
        d = request.json
        if not d.get('date'): return jsonify([])
        organizer_id = int(session['user_id'])
        participant_id = int(d.get('participant_id') or 0)
        duration = int(d.get('duration', 1))
        
        slots, curr = [], 9 
        while curr + duration <= 18:
            s_dt = f"{d['date']} {curr:02d}:00:00"
            e_dt = f"{d['date']} {curr+duration:02d}:00:00"
            display = f"{curr:02d}:00 - {curr+duration:02d}:00"
            curr += duration
            q = f"""SELECT * FROM meetings WHERE (organizer_id=%s OR participant_id=%s OR organizer_id=%s OR participant_id=%s) AND status!='cancelled' AND (start_time < '{e_dt}' AND end_time > '{s_dt}')"""
            conflict = fetch_query(q, (organizer_id, organizer_id, participant_id, participant_id))
            status = "booked" if conflict else "available"
            slots.append({"display": display, "full_start": s_dt, "full_end": e_dt, "status": status})
        return jsonify(slots)
    except: return jsonify([])

@app.route('/api/schedule', methods=['POST'])
def schedule():
    d = request.json
    try:
        s = datetime.fromisoformat(d['start_time'])
        e = datetime.fromisoformat(d['end_time'])
        organizer = int(session['user_id'])
        participant = int(d['participant_id'])
        
        # --- FIX: Ensure Invite Type is captured and lowercase ---
        inv_type = d.get('invite_type', 'person').lower() 

        q = f"""SELECT * FROM meetings WHERE (organizer_id=%s OR participant_id=%s OR organizer_id=%s OR participant_id=%s) AND status!='cancelled' AND (start_time < '{e}' AND end_time > '{s}')"""
        if fetch_query(q, (organizer, organizer, participant, participant)):
             return jsonify({"status":"conflict", "message":"Time Slot Just Taken!"})

        execute_query("INSERT INTO meetings (title, organizer_id, participant_id, start_time, end_time, location, invite_type) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                     (d['title'], organizer, participant, s, e, d['location'], inv_type))
        
        new_mtg = fetch_query("SELECT meeting_id FROM meetings WHERE title=%s AND organizer_id=%s ORDER BY meeting_id DESC LIMIT 1", (d['title'], organizer))
        part_user = fetch_query("SELECT username FROM users WHERE user_id=%s", (participant,))
        
        return jsonify({
            "status":"success", 
            "meeting_id": new_mtg[0]['meeting_id'] if new_mtg else 0,
            "title": d['title'],
            "participant": part_user[0]['username'] if part_user else "Unknown",
            "start_time": str(s)
        })
    except Exception as e: 
        traceback.print_exc()
        return jsonify({"status":"error", "message":str(e)})

@app.route('/api/cancel', methods=['POST'])
def cancel_meeting():
    d = request.json
    try:
        m = fetch_query("SELECT start_time FROM meetings WHERE meeting_id=%s", (d['meeting_id'],))
        if m and (m[0]['start_time'] - datetime.now() < timedelta(hours=24)) and (m[0]['start_time'] > datetime.now()):
            return jsonify({"status":"error", "message":"Locked: Cannot cancel within 24hrs."})
        execute_query("UPDATE meetings SET status='cancelled', cancellation_reason=%s WHERE meeting_id=%s", (d['reason'], d['meeting_id']))
        return jsonify({"status":"success"})
    except: return jsonify({"status":"error"})

@app.route('/api/update_meeting', methods=['POST'])
def update_meeting():
    d = request.json
    try:
        s = datetime.fromisoformat(f"{d['date']} {d['time']}:00")
        e = s + timedelta(hours=1)
        execute_query("UPDATE meetings SET title=%s, start_time=%s, end_time=%s WHERE meeting_id=%s", (d['title'], s, e, d['meeting_id']))
        return jsonify({"status":"success"})
    except: return jsonify({"status":"error"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)