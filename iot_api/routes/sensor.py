from flask import Blueprint, request, jsonify
from app import db
from models import Sensor
import uuid

bp = Blueprint('sensor', __name__, url_prefix='/api/v1/sensor')


@bp.route('', methods=['GET'])
def get_sensors():
    all_sensors = Sensor.query.all()
    sensors_list = []
    for sensor in all_sensors:
        sensors_list.append({
            'id': sensor.id,
            'location_id': sensor.location_id,
            'sensor_name': sensor.sensor_name,
            'sensor_category': sensor.sensor_category,
            'sensor_meta': sensor.sensor_meta,
            'sensor_api_key': sensor.sensor_api_key
        })
    return jsonify(sensors_list)


@bp.route('', methods=['POST'])
def create_sensor():
    data = request.get_json()
    new_sensor = Sensor(
        location_id=data['location_id'],
        sensor_name=data['sensor_name'],
        sensor_category=data['sensor_category'],
        sensor_meta=data.get('sensor_meta', ''),
        sensor_api_key=str(uuid.uuid4())
    )
    db.session.add(new_sensor)
    db.session.commit()
    return jsonify(new_sensor.id), 201

@bp.route('/<int:id>', methods=['GET'])
def get_sensor(id):
    sensor = Sensor.query.get_or_404(id)
    return jsonify({
        'id': sensor.id,
        'location_id': sensor.location_id,
        'sensor_name': sensor.sensor_name,
        'sensor_category': sensor.sensor_category,
        'sensor_meta': sensor.sensor_meta,
        'sensor_api_key': sensor.sensor_api_key
    })

@bp.route('/<int:id>', methods=['PUT'])
def update_sensor(id):
    data = request.get_json()
    sensor = Sensor.query.get_or_404(id)
    sensor.sensor_name = data.get('sensor_name', sensor.sensor_name)
    sensor.sensor_category = data.get('sensor_category', sensor.sensor_category)
    sensor.sensor_meta = data.get('sensor_meta', sensor.sensor_meta)
    db.session.commit()
    return jsonify({'message': 'Sensor updated'})

@bp.route('/<int:id>', methods=['DELETE'])
def delete_sensor(id):
    sensor = Sensor.query.get_or_404(id)
    db.session.delete(sensor)
    db.session.commit()
    return jsonify({'message': 'Sensor deleted'})
