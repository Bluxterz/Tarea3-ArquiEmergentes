from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///iot_api.db'
db = SQLAlchemy(app)

from routes import company, location, sensor, sensor_data
app.register_blueprint(company.bp)
app.register_blueprint(location.bp)
app.register_blueprint(sensor.bp)
app.register_blueprint(sensor_data.bp)

if __name__ == "__main__":
    app.run(debug=True)
