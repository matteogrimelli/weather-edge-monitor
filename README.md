# Weather Edge Monitor

Weather Edge Monitor è una semplice applicazione web sviluppata con Flask, Docker e AWS.

L'applicazione permette di cercare una città e visualizzare i dati meteo correnti tramite le API pubbliche di Open-Meteo. Il progetto include una dashboard HTML, un endpoint REST, test automatici, containerizzazione Docker e una pipeline CI/CD su AWS.

## Obiettivo

L'obiettivo del progetto è realizzare una piccola applicazione cloud-native con:

- backend Flask
- dashboard HTML
- API REST
- container Docker
- pipeline locale
- deploy automatico su AWS

Il progetto mostra un flusso completo di sviluppo:

    sviluppo locale
    test automatici
    build Docker
    push su GitHub
    pipeline AWS
    deploy su Elastic Beanstalk

## Funzionalità

L'applicazione espone tre endpoint principali.

### Dashboard web

    GET /

Mostra una pagina HTML con un form per inserire il nome di una città e visualizzare i dati meteo correnti.

Esempio locale:

    http://localhost:5000/

### API meteo

    GET /api/weather?city=<nome_citta>

Restituisce i dati meteo correnti in formato JSON.

Esempio:

    http://localhost:5000/api/weather?city=Modena

Esempio di risposta:

    {
      "city": "Modena",
      "country": "Italy",
      "humidity": 60,
      "region": "Emilia-Romagna",
      "temperature": 22.5,
      "time": "2026-07-05T10:00",
      "wind_speed": 7.2
    }

### Health check

    GET /health

Restituisce lo stato dell'applicazione.

Esempio:

    {
      "status": "ok",
      "version": "1.2.0"
    }

## Tecnologie utilizzate

- Python
- Flask
- Requests
- Pytest
- Docker
- Docker Compose
- PowerShell
- Git
- GitHub
- AWS CodePipeline
- AWS CodeBuild
- AWS Elastic Beanstalk
- Gunicorn
- Open-Meteo API

## Architettura

L'applicazione è un servizio web monolitico containerizzato.

La dashboard HTML, l'API REST e l'endpoint di health check sono esposti dalla stessa applicazione Flask ed eseguiti nello stesso container Docker.

Flusso principale:

    Utente
      -> Flask app
      -> Open-Meteo Geocoding API
      -> Open-Meteo Forecast API
      -> risposta HTML o JSON

L'applicazione usa due chiamate esterne:

1. Geocoding API: converte il nome della città in coordinate geografiche.
2. Forecast API: usa le coordinate per ottenere i dati meteo correnti.

## Struttura del progetto

    weather-edge-monitor/
    ├── app.py
    ├── requirements.txt
    ├── Dockerfile
    ├── docker-compose.yml
    ├── buildspec.yml
    ├── local-pipeline.ps1
    ├── local-deploy.ps1
    ├── README.md
    ├── CHANGELOG.md
    ├── TESTING.md
    ├── templates/
    │   └── index.html
    └── tests/
        └── test_app.py

## Esecuzione locale

Creazione virtual environment:

    python -m venv venv

Attivazione:

    .\venv\Scripts\Activate.ps1

Installazione dipendenze:

    pip install -r requirements.txt

Avvio applicazione:

    python app.py

Applicazione disponibile su:

    http://localhost:5000/

## Test

Esecuzione dei test:

    python -m pytest

I test verificano gli endpoint principali e simulano le chiamate a Open-Meteo per non dipendere dalla rete durante la pipeline.

## Docker

Build immagine:

    docker build -t weather-edge-monitor .

Avvio container:

    docker run -d --name weather-edge-monitor -p 5000:5000 weather-edge-monitor

Applicazione disponibile su:

    http://localhost:5000/

## Pipeline locale

Il progetto contiene due script PowerShell.

### local-pipeline.ps1

Esegue una pipeline locale di validazione:

    test
    build Docker
    avvio container temporaneo
    health check
    cleanup

Comando:

    .\local-pipeline.ps1

### local-deploy.ps1

Esegue un deploy locale persistente:

    test
    build Docker
    rimozione vecchio container
    avvio nuovo container
    health check

Comando:

    .\local-deploy.ps1

Questo script lascia il container attivo per testare manualmente l'applicazione dal browser.

## Workflow Git

Il progetto usa un workflow basato su branch:

- `main`: versione stabile e deployabile
- `develop`: branch di integrazione
- `feature/*`: nuove funzionalità
- `bugfix/*`: correzioni

Flusso tipico:

    feature branch
      -> merge in develop
      -> merge in main
      -> push su main
      -> deploy automatico AWS

## Pipeline AWS

La pipeline cloud è composta da:

    GitHub
      -> AWS CodePipeline
      -> AWS CodeBuild
      -> AWS Elastic Beanstalk

Ogni push su `main` attiva automaticamente la pipeline.

CodeBuild esegue i test e prepara l'artefatto di deploy.

Elastic Beanstalk esegue l'applicazione containerizzata in cloud.

## URL applicazione

Dashboard online:

    http://weather-edge-monitor-env.eba-dzx73xvh.eu-west-1.elasticbeanstalk.com/

API online:

    http://weather-edge-monitor-env.eba-dzx73xvh.eu-west-1.elasticbeanstalk.com/api/weather?city=Modena

Health check online:

    http://weather-edge-monitor-env.eba-dzx73xvh.eu-west-1.elasticbeanstalk.com/health

## Scelte progettuali

L'applicazione usa un singolo container perché dashboard, API e health check condividono la stessa logica applicativa.

Non è stato usato un database: i dati meteo vengono recuperati in tempo reale dalle API Open-Meteo.

La soluzione è volutamente semplice per ridurre complessità e costi cloud.

## Possibili estensioni future

- HTTPS con certificato TLS
- caching delle risposte meteo
- previsioni su più giorni
- logging strutturato
- monitoraggio con CloudWatch
- separazione frontend/backend
- deploy multi-container
- autenticazione utente
- salvataggio città preferite

## Stato del progetto

Stato attuale:

- applicazione Flask funzionante
- dashboard HTML funzionante
- API REST funzionante
- test automatici funzionanti
- immagine Docker funzionante
- pipeline locale funzionante
- deploy locale persistente funzionante
- pipeline AWS funzionante
- deploy su Elastic Beanstalk funzionante