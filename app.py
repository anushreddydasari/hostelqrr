from flask import Flask, render_template, request
import MySQLdb
import qrcode
import os
import socket
from db_config import db_config

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/qr'

# Ensure the QR folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Function to get local IP address
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't need to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

# Database connection
def get_db_connection():
    return MySQLdb.connect(
        host=db_config['host'],
        user=db_config['user'],
        passwd=db_config['password'],
        db=db_config['database']
    )

@app.route('/')
def home():
    tables = [1, 2, 3, 4, 5]
    return render_template('home.html', tables=tables)

# Generate QR code with actual IP
@app.route('/generate_qr/<int:table_id>')
def generate_qr(table_id):
    local_ip = get_local_ip()
    qr_url = f"http://{local_ip}:5000/menu?table={table_id}"
    qr = qrcode.make(qr_url)

    path = os.path.join(app.config['UPLOAD_FOLDER'], f'table_{table_id}.png')
    qr.save(path)

    return render_template('show_qr.html', table_id=table_id, qr_path=path, qr_url=qr_url)

@app.route('/menu')
def menu():
    table = request.args.get('table')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, price, category FROM menu_items")
    menu_items = cursor.fetchall()
    conn.close()

    return render_template('menu.html', table=table, menu_items=menu_items)

# Run on 0.0.0.0 so other devices can access
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
