FROM python:3.10-slim

WORKDIR /app

# Copiar archivos de requerimientos e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar los archivos necesarios para la aplicación
COPY main.py /app/
COPY ./configure_env /app/configure
COPY ./api /app/api
COPY ./process /app/process
EXPOSE 5000

CMD [ "python", "main.py" ]

