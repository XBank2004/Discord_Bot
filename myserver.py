from flask import Flask
from threading import Thread

app = Flask(__name__)  # ใช้ __name__ แทน ''

@app.route('/')
def home():
    return "Server Is Running!"

def run():
    # ใช้ app.run() โดยกำหนดให้รองรับการเข้าถึงจากทุกที่
    app.run(host='0.0.0.0', port=8080, debug=True)

def server_on():
    t = Thread(target=run)  # สร้าง thread สำหรับการรัน Flask
    t.start()  # เริ่มต้นการทำงานของ thread

# เรียกฟังก์ชัน server_on() เพื่อเริ่มการทำงานของเซิร์ฟเวอร์
if __name__ == "__main__":
    server_on()  # เริ่มต้นเซิร์ฟเวอร์
