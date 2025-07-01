from flask import Blueprint, request, jsonify
from database_manager import (
    add_capture, add_pipeline_output, get_full_analysis_by_url,
    get_all_captures_by_user
)
from pipeline import run_full_pipeline

pipeline_bp = Blueprint('pipeline', __name__)

@pipeline_bp.route('/send-photo', methods=['POST'])
def send_photo():
    data = request.get_json()
    required = ['user_app_id', 'image_url', 'timestamp', 'lat', 'long']
    
    if not all(data.get(field) for field in required):
        return jsonify({"error": "Todos os campos são obrigatórios"}), 400

    capture_id = add_capture(data['user_app_id'], data['image_url'], data['timestamp'], data['lat'], data['long'])
    result = run_full_pipeline(data['image_url'])
    add_pipeline_output(capture_id, result)

    return jsonify(result), 200

@pipeline_bp.route('/get-analysis', methods=['GET'])
def get_analysis():
    image_url = request.args.get('image_url')
    if not image_url:
        return jsonify({"error": "URL da imagem é obrigatória"}), 400
    
    result = get_full_analysis_by_url(image_url)
    if not result:
        return jsonify({"error": "Análise não encontrada"}), 404

    return jsonify(result), 200

@pipeline_bp.route('/user_photos', methods=['GET'])
def user_photos():
    user_app_id = request.args.get('user_app_id')

    if not user_app_id:
        return jsonify({"error": "ID do usuário é obrigatório"}), 400

    try:
        photos = get_all_captures_by_user(int(user_app_id))
    except ValueError:
        return jsonify({"error": "ID do usuário inválido"}), 400

    if not photos:
        return jsonify({"error": "Nenhuma foto encontrada para este usuário"}), 404

    return jsonify(photos), 200
