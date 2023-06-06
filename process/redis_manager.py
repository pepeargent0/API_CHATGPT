import redis
import uuid
import json
import logging

# Configurar el logger
logger = logging.getLogger('redis_manager_logger')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler('redis_manager.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class RedisManager:
    def __init__(self):
        self.redis_client = redis.Redis()
        self.request_queue_key = 'request_queue'

    def enqueue_request(self, request_data, request_id: str = ''):
        try:
            if request_id == '':
                request_id = str(uuid.uuid4())
            request_json = json.dumps(request_data)
            self.redis_client.rpush(self.request_queue_key, request_id)
            self.redis_client.hset(request_id, 'data', request_json)
        except redis.exceptions.RedisError as e:
            raise Exception(f"Error al encolar la solicitud: {str(e)}")

    def dequeue_request(self):
        request_id = self.redis_client.blpop(self.request_queue_key)[1]
        request_json = self.redis_client.hget(request_id, 'data')
        if request_json is not None:
            request_data = json.loads(request_json)  # Convertir desde cadena JSON a dict
            self.redis_client.hdel(request_id, 'data')
            return request_id, request_data
        else:
            return None

    def clear_queue(self):
        try:
            self.redis_client.delete(self.request_queue_key)
        except redis.exceptions.RedisError as e:
            raise Exception(f"Error al limpiar la cola: {str(e)}")

    def check_connection(self):
        try:
            self.redis_client.ping()
        except redis.exceptions.ConnectionError:
            raise Exception("No se pudo establecer la conexión con Redis.")

    def get_result(self, request_id):
        result = self.redis_client.hget(request_id, 'result')
        if result is not None:
            return result.decode('utf-8')
        else:
            return None

    def store_result(self, request_id, result):
        result_json = json.dumps(result)
        self.redis_client.hset(request_id, 'result', result_json)

    @staticmethod
    def log_error(message):
        logger.error(message)

    @staticmethod
    def log_info(message):
        logger.info(message)
