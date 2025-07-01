from flask import Blueprint, jsonify
from src.map.map import gerar_mapa_de_marcadores_html

map_bp = Blueprint('map', __name__)

@map_bp.route('/generate_map', methods=['GET'])
def generate_map():
    map_html = gerar_mapa_de_marcadores_html()

    if not map_html:
        return jsonify({"error": "Nenhum dado encontrado para gerar o mapa"}), 404

    return map_html, 200