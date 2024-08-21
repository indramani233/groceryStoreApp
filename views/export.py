from flask import Blueprint, jsonify
from celery_tasks.export import export_product_details

export_bp = Blueprint('export', __name__)

@export_bp.route('/export/csv')
def trigger_csv_export():
    # Trigger the CSV export task
    export_product_details.delay()

    return jsonify({'message': 'CSV export triggered successfully!'})
