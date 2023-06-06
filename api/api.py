import uuid
import logging

from flask import Blueprint, request, jsonify
from process.redis_manager import RedisManager

api = Blueprint('api', __name__)

redis_manager = RedisManager()

# Configurar el logger
logger = logging.getLogger('api_logger')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler('api.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


@api.route('/api', methods=['GET'])
def api_test():
    return jsonify({'message': 'okey'})


@api.route('/api', methods=['POST'])
def api_endpoint():
    try:
        request_data = request.get_json()
        request_id = str(uuid.uuid4())
        redis_manager.enqueue_request(request_data, request_id)
        logger.info(f"Solicitud recibida correctamente. ID de solicitud: {request_id}")
        return jsonify({'message': 'Solicitud recibida correctamente', 'request_id': request_id})
    except Exception as e:
        logger.error(f"Error en la solicitud: {str(e)}")
        return jsonify({'error': 'Error en la solicitud'})


@api.route('/api/result/<request_id>', methods=['GET'])
def get_result(request_id):
    try:
        result = redis_manager.get_result(request_id)
        if result is None:
            logger.info(f"Resultado no disponible para la solicitud {request_id}")
            return jsonify({'message': 'Resultado no disponible'})
        else:
            logger.info(f"Resultado obtenido para la solicitud {request_id}")
            return jsonify({'result': result})
    except Exception as e:
        logger.error(f"Error al obtener el resultado para la solicitud {request_id}: {str(e)}")
        return jsonify({'error': 'Error al obtener el resultado'})


def log_error(message):
    logger.error(message)


def log_info(message):
    logger.info(message)
