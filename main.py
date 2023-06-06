from flask import Flask
from api.api import api
from process.queue_processor import process_queue
from process.redis_manager import RedisManager
import threading

app = Flask(__name__)
app.register_blueprint(api)

redis_manager = RedisManager()


def run_flask_app():
    try:
        # Verificar la conexión con Redis
        redis_manager.check_connection()
        print("Conexión con Redis establecida correctamente.")
        # Ejecutar la aplicación Flask
        app.run()
    except Exception as e:
        print("Error al establecer la conexión con Redis:", str(e))


if __name__ == '__main__':
    # Iniciar el proceso de la cola en un subproceso separado
    queue_thread = threading.Thread(target=process_queue)
    queue_thread.start()

    # Ejecutar la aplicación Flask en el hilo principal
    run_flask_app()
