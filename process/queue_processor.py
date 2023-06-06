import logging
import openai
from configure.load_env import OpenAPIConfig
from process.openapi_process import Request
from process.redis_manager import RedisManager

# Configurar el logger
logger = logging.getLogger('queue_processor_logger')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler('queue_processor.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

redis_manager = RedisManager()


def process_queue():
    openai.api_key = OpenAPIConfig().get_api_key()
    try:
        logger.info("Inicio del proceso de la cola")
        while True:
            request_data = redis_manager.dequeue_request()
            if request_data:
                request_id, data = request_data
                print(request_id, data)
                if isinstance(data, bytes):
                    data = data.decode('utf-8')
                request_obj = Request(request_id, data)
                logger.info("Procesando solicitud con ID: %s", request_id)
                response = request_obj.process()
                redis_manager.store_result(request_id, response)
                logger.info("Respuesta obtenida para la solicitud con ID %s: %s", request_id, response)
    except Exception as e:
        logger.error("Error en el procesamiento de la cola: %s", str(e))
