import openai
import logging

logger = logging.getLogger('api_logger')


class Request:
    def __init__(self, id, data):
        self.id = id
        self.data = data

    def process(self):
        try:
            # Aquí puedes realizar la interacción con el modelo de chat GPT
            response = openai.Completion.create(
                engine='text-davinci-003',
                prompt=self.data,
                max_tokens=50
            )
            return response.choices[0].text.strip()
        except Exception as e:
            # Manejo de excepciones y registro de errores
            logger.error(f"Error al procesar solicitud {self.id}: {str(e)}")
            return "Error al procesar la solicitud. Por favor, intenta nuevamente."
