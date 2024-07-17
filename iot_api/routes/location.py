from flask import Blueprint, request, jsonify
from app import db
from models import Location

bp = Blueprint('location', __name__, url_prefix='/api/v1/location')

@bp.route('', methods=['POST'])
def create_location():
    data = request.get_json()
    new_location = Location(
        company_id=data['company_id'],
        location_name=data['location_name'],
        location_country=data['location_country'],
        location_city=data['location_city'],
        location_meta=data.get('location_meta', '')
    )
    db.session.add(new_location)
    db.session.commit()
    return jsonify(new_location.id), 201

@bp.route('/<int:id>', methods=['GET'])
def get_location(id):
    location = Location.query.get_or_404(id)
    return jsonify({
        'id': location.id,
        'company_id': location.company_id,
        'location_name': location.location_name,
        'location_country': location.location_country,
        'location_city': location.location_city,
        'location_meta': location.location_meta
    })

@bp.route('/<int:id>', methods=['PUT'])
def update_location(id):
    data = request.get_json()
    location = Location.query.get_or_404(id)
    location.location_name = data.get('location_name', location.location_name)
    location.location_country = data.get('location_country', location.location_country)
    location.location_city = data.get('location_city', location.location_city)
    location.location_meta = data.get('location_meta', location.location_meta)
    db.session.commit()
    return jsonify({'message': 'Location updated'})

@bp.route('/<int:id>', methods=['DELETE'])
def delete_location(id):
    location = Location.query.get_or_404(id)
    db.session.delete(location)
    db.session.commit()
    return jsonify({'message': 'Location deleted'})
