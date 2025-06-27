from flask import Blueprint, request, jsonify, send_from_directory
from src.models import db
from src.models.user import User
from src.routes.auth import auth_bp
from src.routes.patient import patient_bp
from src.routes.medical_record import medical_record_bp
from src.routes.appointment import appointment_bp
from src.routes.billing import billing_bp
from src.routes.insurance import insurance_bp
from src.routes.hmo import hmo_bp
from src.routes.claim import claim_bp
from src.routes.reconciliation import reconciliation_bp
from src.routes.reporting import reporting_bp
import os

def register_routes(app):
    # Register all blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(patient_bp, url_prefix='/api/patients')
    app.register_blueprint(medical_record_bp, url_prefix='/api/medical-records')
    app.register_blueprint(appointment_bp, url_prefix='/api/appointments')
    app.register_blueprint(billing_bp, url_prefix='/api/billing')
    app.register_blueprint(insurance_bp, url_prefix='/api/insurance')
    app.register_blueprint(hmo_bp, url_prefix='/api/hmo')
    app.register_blueprint(claim_bp, url_prefix='/api/claims')
    app.register_blueprint(reconciliation_bp, url_prefix='/api/reconciliation')
    app.register_blueprint(reporting_bp, url_prefix='/api/reports')
    
    # Create a main blueprint for general routes
    main_bp = Blueprint('main', __name__)
    
    @main_bp.route('/')
    def index():
        return jsonify({
            'message': 'EMR System API',
            'version': '1.0',
            'modules': [
                'Authentication',
                'Patient Management',
                'Medical Records',
                'Appointments',
                'Billing',
                'Insurance',
                'HMO Management',
                'Claims Processing',
                'Reconciliation',
                'Reporting'
            ]
        })
    
    @main_bp.route('/health')
    def health_check():
        return jsonify({'status': 'healthy'})
    
    app.register_blueprint(main_bp, url_prefix='/api')
    
    # Serve static files
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        static_folder_path = app.static_folder
        if static_folder_path is None:
            return "Static folder not configured", 404

        if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
            return send_from_directory(static_folder_path, path)
        else:
            index_path = os.path.join(static_folder_path, 'index.html')
            if os.path.exists(index_path):
                return send_from_directory(static_folder_path, 'index.html')
            else:
                return "index.html not found", 404
