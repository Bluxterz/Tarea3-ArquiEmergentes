from flask import Blueprint, request, jsonify
from app import db
from models import Sensor, SensorData
from models import Company
import time

bp = Blueprint('sensor_data', __name__, url_prefix='/api/v1/sensor_data')

@bp.route('', methods=['POST'])
def create_sensor_data():
    data = request.get_json()
    api_key = data.get('api_key')
    sensor = Sensor.query.filter_by(sensor_api_key=api_key).first()

    if not sensor:
        return jsonify({'error': 'Invalid API key'}), 400

    for entry in data.get('json_data', []):
        sensor_data = SensorData(
            sensor_id=sensor.id,
            data=entry,
            timestamp=int(time.time())
        )
        db.session.add(sensor_data)

    db.session.commit()
    return jsonify({'message': 'Sensor data created'}), 201

@bp.route('', methods=['GET'])
def get_sensor_data():
    api_key = request.args.get('company_api_key')
    from_time = request.args.get('from')
    to_time = request.args.get('to')
    sensor_ids = request.args.getlist('sensor_id')

    company = Company.query.filter_by(company_api_key=api_key).first()

    if not company:
        return jsonify({'error': 'Invalid API key'}), 400

    sensor_data = SensorData.query.filter(
        SensorData.sensor_id.in_(sensor_ids),
        SensorData.timestamp.between(from_time, to_time)
    ).all()

    return jsonify([data.to_dict() for data in sensor_data])
