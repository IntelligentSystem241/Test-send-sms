from flask import Flask, jsonify
import threading
import requests
import json
import base64
import time
from datetime import datetime

app = Flask(__name__)

# --- Cấu hình thông tin cố định ---
TOKEN = 'VSwbgZoWdyz3C3N9AiHJfaEReP0wWuYV'
PHONE = '84327328696'
SENDER_ID = 'c660f859b35d5493'

# --- Hàm gửi SMS ---
def send_sms_gateway(token_plain, phone, content, sender):
    token_raw = token_plain + ":"
    token_encoded = base64.b64encode(token_raw.encode()).decode()

    url = "https://api.speedsms.vn/index.php/sms/send"
    headers = {
        "Authorization": f"Basic {token_encoded}",
        "Content-Type": "application/json"
    }
    payload = {
        "to": [phone],
        "content": content,
        "type": 4,
        "sender": sender
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    print(f"[{datetime.now()}] SMS sent - Status: {response.status_code}")
    return response.status_code, response.json()

# --- Background task gửi SMS mỗi 1 tiếng ---
def background_sms_task():
    while True:
        now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        message = f"[{now_str}] Đây là tin nhắn tự động từ SpeedSMS Gateway."

        try:
            status_code, api_response = send_sms_gateway(TOKEN, PHONE, message, SENDER_ID)
            print(f"Sent SMS at {now_str} | Response: {api_response}")
        except Exception as e:
            print(f"Error sending SMS: {e}")

        # Đợi 1 tiếng (3600 giây)
        time.sleep(3600)

# --- API test (để Render không bị stop) ---
@app.route('/')
def index():
    return jsonify({'status': 'App is running', 'time': datetime.now().isoformat()})

# --- Main ---
if __name__ == '__main__':
    # Chạy background task song song
    threading.Thread(target=background_sms_task, daemon=True).start()

    # Chạy Flask web server
    app.run(host='0.0.0.0', port=5000)
