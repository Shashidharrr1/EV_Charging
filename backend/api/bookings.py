from flask import Blueprint, request, jsonify
from datetime import datetime
from backend.utils.database import Database
from backend.utils.auth import token_required

bookings_bp = Blueprint('bookings', __name__)

@bookings_bp.route('/', methods=['POST'])
@token_required
def create_booking(current_user):
    db = Database.get_connection()
    cursor = db.cursor(dictionary=True)
    data = request.get_json()

    # Check if charging point is available
    cursor.execute("""
        SELECT * FROM charging_points 
        WHERE id = %s AND status = 'available'
    """, (data['charging_point_id'],))
    if not cursor.fetchone():
        cursor.close()
        db.close()
        return jsonify({'message': 'Charging point not available'}), 400

    # Create booking
    cursor.execute("""
        INSERT INTO bookings (user_id, charging_point_id, booking_time, duration) 
        VALUES (%s, %s, %s, %s)
    """, (current_user['user_id'], data['charging_point_id'], 
           data['booking_time'], data['duration']))
    
    # Update charging point status
    cursor.execute("""
        UPDATE charging_points 
        SET status = 'occupied' 
        WHERE id = %s
    """, (data['charging_point_id'],))
    
    db.commit()
    cursor.close()
    db.close()

    return jsonify({'message': 'Booking created successfully'}), 201

@bookings_bp.route('/user', methods=['GET'])
@token_required
def get_user_bookings(current_user):
    db = Database.get_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT b.*, cp.type, cp.power_output, bk.name as bunk_name, 
               bk.address as bunk_address 
        FROM bookings b 
        JOIN charging_points cp ON b.charging_point_id = cp.id 
        JOIN bunks bk ON cp.bunk_id = bk.id
        WHERE b.user_id = %s
        ORDER BY b.booking_time DESC
    """, (current_user['user_id'],))
    
    bookings = cursor.fetchall()
    cursor.close()
    db.close()
    
    return jsonify(bookings)

@bookings_bp.route('/station/<int:bunk_id>', methods=['GET'])
@token_required
def get_station_bookings(current_user, bunk_id):
    db = Database()
    
    # Verify bunk ownership
    result = db.query("SELECT id FROM bunks WHERE id = %s AND owner_id = %s", 
                     (bunk_id, current_user['user_id']))
    if not result.fetchone():
        db.close()
        return jsonify({'message': 'Unauthorized'}), 401

    # Get bookings
    result = db.query("""
        SELECT b.*, u.username, cp.type, cp.power_output 
        FROM bookings b 
        JOIN users u ON b.user_id = u.id 
        JOIN charging_points cp ON b.charging_point_id = cp.id 
        WHERE cp.bunk_id = %s 
        ORDER BY b.booking_time DESC
    """, (bunk_id,))
    bookings = result.fetchall()
    db.close()
    return jsonify(bookings)

@bookings_bp.route('/<int:booking_id>', methods=['PUT'])
@token_required
def update_booking_status(current_user, booking_id):
    db = Database()
    data = request.get_json()

    # Verify booking ownership or bunk ownership
    result = db.query("""
        SELECT b.*, cp.bunk_id 
        FROM bookings b 
        JOIN charging_points cp ON b.charging_point_id = cp.id 
        JOIN bunks bk ON cp.bunk_id = bk.id 
        WHERE b.id = %s AND (b.user_id = %s OR bk.owner_id = %s)
    """, (booking_id, current_user['user_id'], current_user['user_id']))
    booking = result.fetchone()
    
    if not booking:
        db.close()
        return jsonify({'message': 'Unauthorized'}), 401

    # Update booking status
    db.query("""
        UPDATE bookings 
        SET status = %s 
        WHERE id = %s
    """, (data['status'], booking_id))

    # Update charging point status if booking is completed or cancelled
    if data['status'] in ['completed', 'cancelled']:
        db.query("""
            UPDATE charging_points 
            SET status = 'available' 
            WHERE id = %s
        """, (booking['charging_point_id'],))

    db.commit()
    db.close()

    return jsonify({'message': 'Booking updated successfully'})