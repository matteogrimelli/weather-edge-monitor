# Importa Flask, il framework web usato per creare l'applicazione.
# jsonify serve per restituire risposte in formato JSON.
from flask import Flask, jsonify


# Crea l'istanza principale dell'applicazione Flask.
# __name__ indica a Flask il modulo corrente, utile per configurare percorsi e risorse.
app = Flask(__name__)


# Versione corrente dell'applicazione.
# Verrà mostrata sia nella homepage sia nell'endpoint /health.
APP_VERSION = "1.0.0"


# Definisce la route principale dell'applicazione.
# Quando l'utente apre http://localhost:5000/, viene eseguita questa funzione.
@app.route("/")
def home():
    # Restituisce una semplice pagina HTML.
    # Questa è la prima versione minimale della dashboard.
    return """
    <html>
        <head>
            <title>Weather Edge Monitor</title>
        </head>
        <body>
            <h1>Weather Edge Monitor</h1>
            <p>Base application running successfully.</p>
            <p>Version: 1.0.0</p>
        </body>
    </html>
    """


# Definisce l'endpoint /health.
# Serve per verificare che l'applicazione sia attiva e risponda correttamente.
# Sarà utile anche per Docker, pipeline locale e pipeline AWS.
@app.route("/health")
def health():
    # Restituisce una risposta JSON con stato e versione dell'app.
    return jsonify({
        "status": "ok",
        "version": APP_VERSION
    })


# Questo blocco viene eseguito solo quando il file app.py viene lanciato direttamente.
# Non viene eseguito se l'app viene importata da un altro modulo.
if __name__ == "__main__":
    # Avvia il server Flask.
    # host="0.0.0.0" permette all'app di essere raggiungibile anche dentro Docker.
    # port=5000 indica che l'app sarà disponibile sulla porta 5000.
    app.run(host="0.0.0.0", port=5000)