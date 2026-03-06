import os
import smtplib
from flask import Flask, request, render_template_string, send_from_directory
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# --- THE SETTINGS ---
MY_GMAIL = "favout.com@gmail.com" 
APP_PASSWORD = "app password " 
BRAND_NAME = "Tumise Graphix"
UPLOAD_FOLDER = 'uploads'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# THE HOME ROUTE
@app.route('/')
def index():
    return send_from_directory(BASE_DIR, 'index.html')

def send_mail(to_email, subject, body):
    msg = MIMEMultipart()
    msg['From'], msg['To'], msg['Subject'] = f"{BRAND_NAME} <{MY_GMAIL}>", to_email, subject
    msg.attach(MIMEText(body, 'plain'))
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(MY_GMAIL, APP_PASSWORD)
            server.send_message(msg)
    except Exception as e: print(f"Mail Error: {e}")

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    user_email = request.form.get('email')
    try:
        send_mail(MY_GMAIL, f"New Order: {name}", f"Project received from {name}")
        
        SUCCESS_HTML = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Project Received | Tumise Graphix</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body { background: #f5f5f7; font-family: -apple-system, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; overflow: hidden; }
                .card { background: #ffffff; padding: 60px; border-radius: 24px; box-shadow: 0 10px 40px rgba(0,0,0,0.04); text-align: center; max-width: 450px; border: 1px solid #d2d2d7; }
                .check-icon { width: 80px; height: 80px; background: #0071e3; color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 40px; margin: 0 auto 30px; }
                h1 { font-size: 24px; font-weight: 600; color: #1d1d1f; margin-bottom: 15px; }
                p { font-size: 16px; color: #86868b; line-height: 1.5; margin-bottom: 25px; }
                .status-bar { width: 100%; height: 4px; background: #eee; border-radius: 10px; margin-top: 20px; overflow: hidden; position: relative; }
                .progress { width: 100%; height: 100%; background: #0071e3; position: absolute; left: 0; transition: width 65s linear; }
                .status-text { font-size: 0.75rem; color: #0071e3; font-weight: 600; margin-top: 10px; text-transform: uppercase; }
                #news-box { position: fixed; bottom: 25px; right: -400px; width: 340px; background: #1d1d1f; color: #fff; padding: 22px; border-radius: 18px; box-shadow: 0 15px 45px rgba(0,0,0,0.2); transition: 0.8s; z-index: 9999; text-align: left; }
                #news-box.show { right: 25px; }
            </style>
        </head>
        <body onload="startEngine()">
            <div class="card">
                <div class="check-icon">✓</div>
                <h1>Project Received</h1>
                <p>Project brief recieved. Stay tuned for these elite updates...</p>
                <div class="status-bar"><div id="p-bar" class="progress"></div></div>
                <div class="status-text">Tab will auto-close after updates</div>
            </div>
            <div id="news-box">
                <div id="news-tag" style="font-size: 0.7rem; color: #0071e3; font-weight: 800; margin-bottom: 5px;">UPDATE</div>
                <div id="news-title" style="font-size: 0.95rem; font-weight: 600; margin-bottom: 8px;">Loading...</div>
                <div id="news-body" style="font-size: 0.8rem; color: #d2d2d7;">...</div>
            </div>
            <script>
                const updates = [
                    {tag: "FINANCIAL TRUST 💳", title: "Zero-Deposit Initiation", body: "We accept bank transfers and PayPal. No first deposit required to start a project."},
                    {tag: "NEW SERVICE", title: "3D Motion Graphics 🎬", body: "Launch your brand into the future with our new 3D animation wing."},
                    {tag: "SECURITY", title: "Project Protection 🛡️", body: "Your project references are encrypted and stored on our secure servers."},
                    {tag: "SPEED", title: "24-Hour Delivery ⚡", body: "Our express designer delivers in under 24 hours."},
                    {tag: "QUALITY", title: "4K Vector Resolution 💎", body: "All flyers are exported in ultra-high 4K print-ready format."},
                    {tag: "SUPPORT", title: "24/7 Human Help 📞", body: "Our human team is online 24/7 to support your project contact us now."},
                    {tag: "LOYALTY", title: "Referral Bonus 💰", body: "Refer a friend and get 20% commission on their first order."},
                    {tag: "AI BRANDING", title: "Axel AI Assistant 🦾", body: "Axel is ready to chat about your design status on the home page."},
                    {tag: "PRICING POLICY 📊", title: "Custom Quote project", body: "Costs vary based on complexity and due date you request for it. Launch your brief to receive a custom quote."}
                ];
                let currentIndex = 0;
                const box = document.getElementById('news-box');
                function showNextUpdate() {
                    if (currentIndex >= updates.length) { window.close(); return; }
                    const u = updates[currentIndex];
                    document.getElementById('news-tag').innerText = u.tag;
                    document.getElementById('news-title').innerText = u.title;
                    document.getElementById('news-body').innerText = u.body;
                    box.classList.add('show');
                    setTimeout(() => { box.classList.remove('show'); currentIndex++; setTimeout(showNextUpdate, 1500); }, 5000); 
                }
                function startEngine() {
                    setTimeout(() => { document.getElementById('p-bar').style.width = '0%'; }, 100);
                    setTimeout(showNextUpdate, 2000);
                }
            </script>
        </body>
        </html>
        """
        return render_template_string(SUCCESS_HTML)
    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
