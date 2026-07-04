# Usa come immagine di base Python 3.12 in versione slim.
# La versione slim è più leggera rispetto all'immagine completa.
FROM python:3.12-slim

# Imposta la directory di lavoro interna al container.
# Tutti i comandi successivi verranno eseguiti dentro /app.
WORKDIR /app

# Evita la creazione di file .pyc e cartelle __pycache__ nel container.
ENV PYTHONDONTWRITEBYTECODE=1

# Forza Python a stampare subito i log, senza buffering.
# Utile per vedere correttamente i log del container.
ENV PYTHONUNBUFFERED=1

# Copia il file delle dipendenze dentro il container.
COPY requirements.txt .

# Installa le dipendenze Python definite in requirements.txt.
# --no-cache-dir evita di salvare cache inutile, riducendo la dimensione dell'immagine.
RUN pip install --no-cache-dir -r requirements.txt

# Copia il file principale dell'applicazione dentro il container.
COPY app.py .

# Documenta che l'applicazione usa la porta 5000.
# La porta sarà poi mappata con docker run o docker-compose.
EXPOSE 5000

# Comando eseguito all'avvio del container.
# Avvia l'applicazione Flask.
# CMD ["python", "app.py"]
# Usa Gunicorn come server WSGI per eseguire l'app Flask.
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]