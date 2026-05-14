# =========================================================
#            ĐIỀU KHIỂN LED QUA WEB
# =========================================================
#
# Công nghệ:
#   • Python Flask Web Server
#   • HTML + CSS + JavaScript
#   • Raspberry Pi GPIO
#   • Responsive Dashboard
#
# =========================================================
# CHỨC NĂNG
# =========================================================
#
# • Điều khiển LED qua trình duyệt Web
# • Giao diện hiện đại realtime
# • Hiển thị trạng thái LED
# • Auto refresh trạng thái
# • Nhật ký hệ thống
# • Hỗ trợ Raspberry Pi GPIO
# • Có chế độ giả lập chạy trên Windows
# • Điều khiển từ điện thoại
# • Dashboard Smart Home
#
# =========================================================
# CÀI THƯ VIỆN
# =========================================================
#
# pip install flask
#
# Nếu dùng Raspberry Pi:
# pip install RPi.GPIO
#
# =========================================================
# CÁCH CHẠY
# =========================================================
#
# python app.py
#
# Sau đó mở trình duyệt:
#
# http://127.0.0.1:5000
#
# hoặc:
#
# http://IP_RASPBERRY_PI:5000
#
# =========================================================

from flask import Flask, render_template_string, jsonify
from datetime import datetime
import threading
import time

# =========================================================
# KIỂM TRA RASPBERRY PI GPIO
# =========================================================

IS_RPI = True

try:
    import RPi.GPIO as GPIO
except:
    IS_RPI = False

# =========================================================
# GPIO CONFIG
# =========================================================

LED_PIN = 18

if IS_RPI:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.OUT)

# =========================================================
# APP CONFIG
# =========================================================

app = Flask(__name__)

led_state = False

system_logs = []

# =========================================================
# HTML TEMPLATE
# =========================================================

HTML_PAGE = """

<!DOCTYPE html>
<html lang="vi">

<head>

<meta charset="UTF-8">

<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>SMART LED CONTROL</title>

<style>

body{
    margin:0;
    padding:0;
    background:#0f172a;
    font-family:Arial;
    color:white;
}

.container{
    width:90%;
    margin:auto;
    padding-top:30px;
}

.header{
    text-align:center;
    margin-bottom:30px;
}

.title{
    font-size:40px;
    font-weight:bold;
}

.subtitle{
    color:#94a3b8;
    margin-top:10px;
}

.card{
    background:#1e293b;
    border-radius:20px;
    padding:25px;
    margin-bottom:20px;
    box-shadow:0 0 20px rgba(0,0,0,0.3);
}

.status{
    font-size:30px;
    margin-top:20px;
    font-weight:bold;
}

.on{
    color:#22c55e;
}

.off{
    color:#ef4444;
}

.button-group{
    margin-top:30px;
}

button{
    border:none;
    padding:15px 35px;
    margin:10px;
    border-radius:15px;
    font-size:18px;
    font-weight:bold;
    cursor:pointer;
    transition:0.3s;
}

button:hover{
    transform:scale(1.05);
}

.btn-on{
    background:#22c55e;
    color:white;
}

.btn-off{
    background:#ef4444;
    color:white;
}

.info-grid{
    display:grid;
    grid-template-columns:repeat(auto-fit,minmax(250px,1fr));
    gap:20px;
}

.info-box{
    background:#111827;
    border-radius:15px;
    padding:20px;
}

.log-box{
    background:black;
    color:#22c55e;
    height:250px;
    overflow:auto;
    padding:15px;
    border-radius:10px;
    font-family:Consolas;
}

.footer{
    text-align:center;
    margin-top:30px;
    color:#94a3b8;
}

</style>

</head>

<body>

<div class="container">

    <div class="header">

        <div class="title">
            💡 SMART LED CONTROL
        </div>

        <div class="subtitle">
            Điều khiển LED qua Web bằng Python Flask
        </div>

    </div>

    <div class="card">

        <h2>📌 TRẠNG THÁI LED</h2>

        <div id="status" class="status">
            Loading...
        </div>

        <div class="button-group">

            <button class="btn-on" onclick="turnOn()">
                BẬT LED
            </button>

            <button class="btn-off" onclick="turnOff()">
                TẮT LED
            </button>

        </div>

    </div>

    <div class="info-grid">

        <div class="info-box">

            <h3>⚙ THÔNG TIN HỆ THỐNG</h3>

            <p>Framework: Flask</p>
            <p>GPIO PIN: 18</p>
            <p>Mode:
                {% if is_rpi %}
                    Raspberry Pi GPIO
                {% else %}
                    Simulation Mode
                {% endif %}
            </p>

        </div>

        <div class="info-box">

            <h3>🌐 WEB SERVER</h3>

            <p>Port: 5000</p>
            <p>Realtime Update</p>
            <p>Mobile Support</p>

        </div>

    </div>

    <div class="card">

        <h2>📜 NHẬT KÝ HỆ THỐNG</h2>

        <div class="log-box" id="logs">

        </div>

    </div>

    <div class="footer">
        Smart Home IoT Dashboard - Python Flask
    </div>

</div>

<script>

async function updateStatus(){

    let response = await fetch('/status');

    let data = await response.json();

    let statusDiv = document.getElementById("status");

    if(data.led == true){

        statusDiv.innerHTML = "🟢 LED ĐANG BẬT";
        statusDiv.className = "status on";

    }else{

        statusDiv.innerHTML = "🔴 LED ĐANG TẮT";
        statusDiv.className = "status off";
    }

    let logsDiv = document.getElementById("logs");

    logsDiv.innerHTML = "";

    data.logs.forEach(log => {

        logsDiv.innerHTML += log + "<br>";

    });

}

async function turnOn(){

    await fetch('/on');

    updateStatus();

}

async function turnOff(){

    await fetch('/off');

    updateStatus();

}

setInterval(updateStatus,1000);

updateStatus();

</script>

</body>
</html>

"""

# =========================================================
# HÀM GHI LOG
# =========================================================

def write_log(message):

    current_time = datetime.now().strftime("%H:%M:%S")

    log = f"[{current_time}] {message}"

    system_logs.append(log)

    # Giới hạn log
    if len(system_logs) > 50:
        system_logs.pop(0)

    print(log)

# =========================================================
# ĐIỀU KHIỂN LED
# =========================================================

def set_led(state):

    global led_state

    led_state = state

    if IS_RPI:

        GPIO.output(LED_PIN, state)

    if state:

        write_log("LED đã được BẬT.")

    else:

        write_log("LED đã được TẮT.")

# =========================================================
# ROUTE HOME
# =========================================================

@app.route("/")
def home():

    return render_template_string(
        HTML_PAGE,
        is_rpi=IS_RPI
    )

# =========================================================
# ROUTE BẬT LED
# =========================================================

@app.route("/on")
def led_on():

    set_led(True)

    return jsonify({
        "success": True
    })

# =========================================================
# ROUTE TẮT LED
# =========================================================

@app.route("/off")
def led_off():

    set_led(False)

    return jsonify({
        "success": True
    })

# =========================================================
# ROUTE STATUS
# =========================================================

@app.route("/status")
def status():

    return jsonify({
        "led": led_state,
        "logs": system_logs
    })

# =========================================================
# AUTO SYSTEM MONITOR
# =========================================================

def system_monitor():

    while True:

        time.sleep(15)

        write_log("Web server đang hoạt động bình thường.")

# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    print("=" * 60)
    print("SMART LED CONTROL SYSTEM")
    print("=" * 60)

    print("\n📌 THÔNG TIN HỆ THỐNG")

    if IS_RPI:
        print("✅ Raspberry Pi GPIO: READY")
    else:
        print("⚠ Chạy ở chế độ giả lập Windows")

    print("✅ Flask Web Server: READY")

    print("\n🌐 TRUY CẬP WEB:")
    print("http://127.0.0.1:5000")

    print("\n🚀 KHỞI ĐỘNG SERVER...\n")

    write_log("Hệ thống Smart LED khởi động.")

    monitor_thread = threading.Thread(
        target=system_monitor
    )

    monitor_thread.daemon = True

    monitor_thread.start()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
