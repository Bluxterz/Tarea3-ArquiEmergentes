from datetime import datetime
from flask import Blueprint, request, jsonify
from app import db
from models import SensorData, Sensor, Company
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
    company_api_key = request.args.get('company_api_key')
    from_timestamp = request.args.get('from')
    to_timestamp = request.args.get('to')
    sensor_ids = request.args.getlist('sensor_id')

    # Validar la compañía con el API key proporcionado
    if not company_api_key:
        return jsonify({'error': 'Company API key is required'}), 400

    # Aquí deberías validar el API key de la compañía según tu implementación actual
    # Suponiendo que tienes una función para validar el API key de la compañía

    # Filtrar los datos de sensor según los parámetros
    query = SensorData.query

    if from_timestamp:
        query = query.filter(SensorData.timestamp >= int(from_timestamp))

    if to_timestamp:
        query = query.filter(SensorData.timestamp <= int(to_timestamp))

    if sensor_ids:
        query = query.filter(SensorData.sensor_id.in_(sensor_ids))

    sensor_data = query.all()

    result = []
    for data in sensor_data:
        result.append({
            'id': data.id,
            'sensor_id': data.sensor_id,
            'data': data.data,
            'timestamp': data.timestamp
        })
    return jsonify(result)