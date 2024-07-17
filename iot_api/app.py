# app.py
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///iot_api.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    with app.app_context():
        from models import Company  # Importar aquí para que se registre en el contexto
        
        from routes.company import bp as company_bp
        from routes.location import bp as location_bp
        from routes.sensor import bp as sensor_bp
        from routes.sensor_data import bp as sensor_data_bp
        
        app.register_blueprint(company_bp)
        app.register_blueprint(location_bp)
        app.register_blueprint(sensor_bp)
        app.register_blueprint(sensor_data_bp)
        
        # Crear todas las tablas (si no existen)
        db.create_all()

        # Ruta para servir index.html (opcional, si lo necesitas)
        @app.route('/')
        def index():
            return render_template('index.html')

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

