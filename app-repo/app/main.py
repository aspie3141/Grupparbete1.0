import os
import time
import socket
import pymysql

from flask import Flask, jsonify, request

app = Flask(__name__)

hostname = socket.gethostname()

DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'mariadb'),
    'port': int(os.environ.get('DB_PORT', 3306)),
    'user': os.environ.get('DB_USER', 'app_user'),
    'password': os.environ.get('DB_PASSWORD', 'secure_password_123'),
    'database': os.environ.get('DB_NAME', 'app_db'),
    'cursorclass': pymysql.cursors.DictCursor,
}


def get_db():
    return pymysql.connect(**DB_CONFIG)


def wait_for_db(retries=30, delay=2):
    for i in range(retries):
        try:
            conn = get_db()
            conn.close()
            print(f"[{hostname}] Databasanslutning lyckades.")
            return
        except pymysql.err.OperationalError:
            print(f"[{hostname}] Väntar på databasen... ({i+1}/{retries})")
            time.sleep(delay)
    raise RuntimeError("Kunde inte ansluta till databasen.")


@app.before_request
def block_methods():
    if request.method in ('DELETE', 'HEAD'):
        return jsonify({
            'hostname': hostname,
            'error': f'Metoden {request.method} är inte tillåten'
        }), 405


@app.route('/health', methods=['GET'])
def health():
    try:
        conn = get_db()
        conn.close()
        return jsonify({'hostname': hostname, 'status': 'healthy', 'database': 'connected'})
    except Exception as e:
        return jsonify({'hostname': hostname, 'status': 'unhealthy', 'database': str(e)}), 500


@app.route('/items', methods=['GET'])
def get_items():
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM items')
            items = cur.fetchall()
        return jsonify({'hostname': hostname, 'data': items})
    finally:
        conn.close()


@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM items WHERE id = %s', (item_id,))
            item = cur.fetchone()
        if item is None:
            return jsonify({'hostname': hostname, 'error': 'Objektet hittades inte'}), 404
        return jsonify({'hostname': hostname, 'data': item})
    finally:
        conn.close()


@app.route('/items', methods=['POST'])
def create_item():
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'hostname': hostname, 'error': 'Fältet "name" krävs'}), 400

    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute(
                'INSERT INTO items (name, description) VALUES (%s, %s)',
                (data['name'], data.get('description', ''))
            )
            conn.commit()
            new_id = cur.lastrowid
            cur.execute('SELECT * FROM items WHERE id = %s', (new_id,))
            item = cur.fetchone()
        return jsonify({'hostname': hostname, 'data': item}), 201
    finally:
        conn.close()


@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.get_json()
    if not data:
        return jsonify({'hostname': hostname, 'error': 'Ingen data skickades'}), 400

    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM items WHERE id = %s', (item_id,))
            if cur.fetchone() is None:
                return jsonify({'hostname': hostname, 'error': 'Objektet hittades inte'}), 404

            name = data.get('name')
            description = data.get('description')

            if name and description is not None:
                cur.execute('UPDATE items SET name=%s, description=%s WHERE id=%s',
                            (name, description, item_id))
            elif name:
                cur.execute('UPDATE items SET name=%s WHERE id=%s', (name, item_id))
            elif description is not None:
                cur.execute('UPDATE items SET description=%s WHERE id=%s',
                            (description, item_id))
            conn.commit()

            cur.execute('SELECT * FROM items WHERE id = %s', (item_id,))
            item = cur.fetchone()
        return jsonify({'hostname': hostname, 'data': item})
    finally:
        conn.close()


if __name__ == '__main__':
    wait_for_db()
    app.run(host='0.0.0.0', port=5000)
