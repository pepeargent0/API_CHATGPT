import os
from dotenv import load_dotenv
import logging

# Configurar el logger
logger = logging.getLogger('openapi_config_logger')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler('openapi_config.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class OpenAPIConfig:
    def __init__(self):
        try:
            load_dotenv()
            self.api_key = os.getenv('OPENAPI_KEY')
        except Exception as e:
            self.log_error(f"Error al cargar la configuración de OpenAPI: {str(e)}")

    def get_api_key(self):
        return self.api_key

    @staticmethod
    def log_error(message):
        logger.error(message)

    @staticmethod
    def log_info(message):
        logger.info(message)
