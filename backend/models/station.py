from backend.utils.database import Database

class Station:
    def __init__(self, id, name, address, latitude, longitude, owner_id):
        self.id = id
        self.name = name
        self.address = address
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id

    @staticmethod
    def get_by_id(station_id):
        db = Database.get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute('SELECT * FROM bunks WHERE id = %s', (station_id,))
        result = cursor.fetchone()
        cursor.close()
        db.close()
        
        if result:
            return Station(
                id=result['id'],
                name=result['name'],
                address=result['address'],
                latitude=result['latitude'],
                longitude=result['longitude'],
                owner_id=result['owner_id']
            )
        return None

    @staticmethod
    def get_all():
        db = Database.get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute('SELECT * FROM bunks')
        results = cursor.fetchall()
        cursor.close()
        db.close()
        
        return [Station(
            id=row['id'],
            name=row['name'],
            address=row['address'],
            latitude=row['latitude'],
            longitude=row['longitude'],
            owner_id=row['owner_id']
        ) for row in results]

    @staticmethod
    def create(data):
        db = Database.get_connection()
        cursor = db.cursor()
        cursor.execute(
            'INSERT INTO bunks (name, address, latitude, longitude, owner_id) VALUES (%s, %s, %s, %s, %s)',
            (data['name'], data['address'], data['latitude'], data['longitude'], data['owner_id'])
        )
        station_id = cursor.lastrowid
        db.commit()
        cursor.close()
        db.close()
        
        return Station.get_by_id(station_id)