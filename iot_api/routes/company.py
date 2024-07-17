from flask import Blueprint, request, jsonify
from app import db
from models import Company
import uuid

bp = Blueprint('company', __name__, url_prefix='/api/v1/company')


@bp.route('', methods=['POST'])
def create_company():
    data = request.get_json()
    new_company = Company(
        company_name=data['company_name'],
        company_api_key=str(uuid.uuid4())
    )
    db.session.add(new_company)
    db.session.commit()
    # Retorna un objeto JSON con todos los detalles de la nueva compañía
    return jsonify({
        'id': new_company.id,
        'company_name': new_company.company_name,
        'company_api_key': new_company.company_api_key
    }), 201

@bp.route('', methods=['GET'])
def get_companies():
    all_companies = Company.query.all()
    companies_list = []
    for company in all_companies:
        companies_list.append({
            'id': company.id,
            'company_name': company.company_name,
            'company_api_key': company.company_api_key
        })
    return jsonify(companies_list)


@bp.route('/<int:id>', methods=['PUT'])
def update_company(id):
    data = request.get_json()
    company = Company.query.get_or_404(id)
    company.company_name = data.get('company_name', company.company_name)
    db.session.commit()
    # Retorna un objeto JSON con un mensaje indicando que la compañía ha sido actualizada
    return jsonify({'message': 'Company updated', 'id': company.id}), 200

@bp.route('/<int:id>', methods=['DELETE'])
def delete_company(id):
    company = Company.query.get_or_404(id)
    db.session.delete(company)
    db.session.commit()
    return jsonify({'message': 'Company deleted'})
