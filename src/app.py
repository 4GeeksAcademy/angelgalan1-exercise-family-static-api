"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Crear el objeto de la familia Jackson
jackson_family = FamilyStructure("Jackson")

# Manejador de errores personalizados en formato JSON
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# Ruta principal que genera un sitemap con todos los endpoints disponibles
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# Obtener todos los miembros de la familia
@app.route('/members', methods=['GET'])
def get_all_members():
    try:
        members = jackson_family.get_all_members()
        return jsonify(members), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Obtener un solo miembro según su ID
@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    member = jackson_family.get_member(member_id)
    if member:
        return jsonify(member), 200
    return jsonify({"error": "Miembro no encontrado"}), 404

# Agregar un nuevo miembro a la familia
@app.route('/member', methods=['POST'])
def add_member():
    try:
        data = request.get_json()
        # Verifica que los campos obligatorios estén presentes
        if not all(k in data for k in ("first_name", "age", "lucky_numbers")):
            return jsonify({"error": "Faltan campos obligatorios"}), 400
        new_member = jackson_family.add_member(data)
        return jsonify(new_member), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Eliminar un miembro de la familia por ID
@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    deleted = jackson_family.delete_member(member_id)
    if deleted:
        return jsonify({"done": True}), 200
    return jsonify({"error": "Miembro no encontrado"}), 404

# Ejecutar el servidor solo si se llama directamente el archivo
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
