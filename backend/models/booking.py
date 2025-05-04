from backend.utils.database import Database
from backend.models.station import Station

class Booking:
    def __init__(self, id, user_id, station_id, charging_point_id, start_time, end_time, status):
        self.id = id
        self.user_id = user_id
        self.station_id = station_id
        self.charging_point_id = charging_point_id
        self.start_time = start_time
        self.end_time = end_time
        self.status = status

    @staticmethod
    def get_by_id(booking_id):
        db = Database.get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            'SELECT * FROM bookings WHERE id = %s',
            (booking_id,)
        )
        result = cursor.fetchone()
        cursor.close()
        db.close()

        if result:
            return Booking(
                id=result['id'],
                user_id=result['user_id'],
                station_id=result['station_id'],
                charging_point_id=result['charging_point_id'],
                start_time=result['start_time'],
                end_time=result['end_time'],
                status=result['status']
            )
        return None

    @staticmethod
    def get_user_bookings(user_id):
        db = Database.get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            'SELECT * FROM bookings WHERE user_id = %s ORDER BY start_time DESC',
            (user_id,)
        )
        results = cursor.fetchall()
        cursor.close()
        db.close()

        return [Booking(
            id=row['id'],
            user_id=row['user_id'],
            station_id=row['station_id'],
            charging_point_id=row['charging_point_id'],
            start_time=row['start_time'],
            end_time=row['end_time'],
            status=row['status']
        ) for row in results]

    @staticmethod
    def create(data):
        db = Database.get_connection()
        cursor = db.cursor()
        cursor.execute(
            'INSERT INTO bookings (user_id, station_id, charging_point_id, start_time, end_time, status) VALUES (%s, %s, %s, %s, %s, %s)',
            (data['user_id'], data['station_id'], data['charging_point_id'], data['start_time'], data['end_time'], 'pending')
        )
        booking_id = cursor.lastrowid
        db.commit()
        cursor.close()
        db.close()

        return Booking.get_by_id(booking_id)