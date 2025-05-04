from flask import Blueprint

# Create blueprints
api_bp = Blueprint('api', __name__)
auth_bp = Blueprint('auth', __name__)
stations_bp = Blueprint('stations', __name__)
bookings_bp = Blueprint('bookings', __name__)

# Import routes
from . import auth, stations, bookings

# Register blueprints
api_bp.register_blueprint(auth_bp, url_prefix='/auth')
api_bp.register_blueprint(stations_bp, url_prefix='/stations')
api_bp.register_blueprint(bookings_bp, url_prefix='/bookings')

# Export the main blueprint
__all__ = ['api_bp']