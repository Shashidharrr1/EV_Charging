from flask import Blueprint, request, jsonify
from backend.utils.database import Database
from backend.utils.auth import token_required

stations_bp = Blueprint('stations', __name__)

@stations_bp.route('/', methods=['GET'])
def get_stations():
    db = Database.get_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT b.*, cp.id as point_id, cp.type, cp.power_output, 
               cp.status, cp.price_per_kwh 
        FROM bunks b 
        JOIN charging_points cp ON b.id = cp.bunk_id
        WHERE cp.status = 'available'
    """)
    stations = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify(stations)

@stations_bp.route('/<int:station_id>', methods=['GET'])
def get_station(station_id):
    db = Database.get_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT b.*, cp.id as point_id, cp.type, cp.power_output, 
               cp.status, cp.price_per_kwh 
        FROM bunks b 
        JOIN charging_points cp ON b.id = cp.bunk_id 
        WHERE b.id = %s
    """, (station_id,))
    station = cursor.fetchone()
    cursor.close()
    db.close()
    
    if not station:
        return jsonify({'message': 'Station not found'}), 404
    return jsonify(station)

@stations_bp.route('/charging-points', methods=['POST'])
@token_required
def add_charging_point(current_user):
    db = Database.get_connection()
    cursor = db.cursor(dictionary=True)
    data = request.get_json()

    # Verify bunk ownership
    cursor.execute("SELECT id FROM bunks WHERE id = %s AND owner_id = %s", 
                  (data['bunk_id'], current_user['user_id']))
    if not cursor.fetchone():
        cursor.close()
        db.close()
        return jsonify({'message': 'Unauthorized'}), 401

    # Add charging point
    cursor.execute("""
        INSERT INTO charging_points 
        (bunk_id, type, power_output, status, price_per_kwh) 
        VALUES (%s, %s, %s, 'available', %s)
    """, (data['bunk_id'], data['type'], data['power_output'], data['price_per_kwh']))
    db.commit()
    
    new_point_id = cursor.lastrowid
    cursor.close()
    db.close()
    
    return jsonify({
        'message': 'Charging point added successfully',
        'point_id': new_point_id
    }), 201

@stations_bp.route('/charging-points/<int:point_id>', methods=['PUT'])
@token_required
def update_charging_point(current_user, point_id):
    db = Database.get_connection()
    cursor = db.cursor(dictionary=True)
    data = request.get_json()

    # Verify bunk ownership
    cursor.execute("""
        SELECT b.id FROM bunks b 
        JOIN charging_points cp ON b.id = cp.bunk_id 
        WHERE cp.id = %s AND b.owner_id = %s
    """, (point_id, current_user['user_id']))
    if not cursor.fetchone():
        cursor.close()
        db.close()
        return jsonify({'message': 'Unauthorized'}), 401

    # Update charging point
    cursor.execute("""
        UPDATE charging_points 
        SET status = %s, price_per_kwh = %s 
        WHERE id = %s
    """, (data['status'], data['price_per_kwh'], point_id))
    db.commit()
    cursor.close()
    db.close()

    return jsonify({'message': 'Charging point updated successfully'})