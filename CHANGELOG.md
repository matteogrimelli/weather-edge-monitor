# Changelog

Questo file riassume l'evoluzione del progetto Weather Edge Monitor.

La struttura è organizzata per versioni dell'applicazione, feature branch e commit principali.

## v1.2.0 - Dashboard HTML

Obiettivo: aggiungere una dashboard web con form per cercare una città e visualizzare i dati meteo in modo leggibile.

Albero delle modifiche:

    v1.2.0
    └── feature/dashboard
        └── Add HTML weather dashboard

### feature/dashboard

Commit principale:

    Add HTML weather dashboard

Modifiche introdotte:

- aggiunta dashboard HTML sulla route `/`
- aggiunto template `templates/index.html`
- aggiunto form per inserire il nome della città
- visualizzazione di temperatura, umidità, vento e orario della rilevazione
- aggiornata versione applicazione a `1.2.0`
- aggiornata logica Flask con `render_template`
- aggiunto test della dashboard con città simulata
- aggiornato `Dockerfile` per copiare la cartella `templates`

File principali:

- `app.py`
- `Dockerfile`
- `tests/test_app.py`
- `templates/index.html`

Test eseguiti:

- `python -m pytest`
- `.\local-deploy.ps1`
- `.\local-pipeline.ps1`

Risultato:

- dashboard funzionante in locale
- dashboard funzionante in Docker
- dashboard funzionante su AWS Elastic Beanstalk

## v1.1.0 - API meteo Open-Meteo

Obiettivo: aggiungere un endpoint REST per ottenere i dati meteo correnti di una città usando Open-Meteo.

Albero delle modifiche:

    v1.1.0
    └── feature/weather-api
        ├── Add Open-Meteo weather API endpoint
        └── Add persistent local deploy script

### feature/weather-api

Commit principale:

    Add Open-Meteo weather API endpoint

Modifiche introdotte:

- aggiunto endpoint `/api/weather`
- aggiunto parametro query `city`
- integrata Open-Meteo Geocoding API
- integrata Open-Meteo Forecast API
- conversione del nome città in coordinate geografiche
- recupero dati meteo tramite latitudine e longitudine
- restituzione risposta JSON normalizzata
- gestione errore per parametro `city` mancante
- gestione errore per città non trovata
- aggiornata versione applicazione a `1.1.0`
- aggiunti test per endpoint meteo

File principali:

- `app.py`
- `tests/test_app.py`

Risultato:

- endpoint API funzionante in locale
- endpoint API funzionante in Docker
- endpoint API funzionante su AWS Elastic Beanstalk

### Deploy locale persistente

Commit principale:

    Add persistent local deploy script

Modifiche introdotte:

- aggiunto script `local-deploy.ps1`
- aggiunta build Docker locale persistente
- rimozione automatica del vecchio container locale
- avvio di un nuovo container aggiornato
- esecuzione automatica dell'health check
- container lasciato attivo per test manuali da browser

File principali:

- `local-deploy.ps1`

Risultato:

- possibilità di testare l'app in Docker senza usare `python app.py`
- container locale persistente funzionante

## v1.0.0 - Applicazione base, Docker e pipeline

Obiettivo: creare la prima versione funzionante dell'applicazione, containerizzarla e configurare pipeline locale e cloud.

Albero delle modifiche:

    v1.0.0
    ├── feature/project-setup
    │   └── Initialize project repository
    ├── feature/base-app
    │   └── Add base Flask application
    ├── feature/docker
    │   ├── Add Docker ignore file
    │   ├── Add Dockerfile for Flask application
    │   └── Add Docker Compose configuration
    ├── feature/local-pipeline
    │   └── Add local pipeline and tests
    └── feature/aws-pipeline
        └── Add AWS CodeBuild configuration

### feature/project-setup

Commit principale:

    Initialize project repository

Modifiche introdotte:

- inizializzato repository Git
- creata struttura iniziale del progetto
- creati branch principali `main` e `develop`
- collegato repository GitHub

File principali:

- `README.md`
- `.gitignore`

### feature/base-app

Commit principale:

    Add base Flask application

Modifiche introdotte:

- creata applicazione Flask base
- aggiunta route `/`
- aggiunta route `/health`
- aggiunta variabile `APP_VERSION`
- aggiunto file delle dipendenze Python

File principali:

- `app.py`
- `requirements.txt`

Endpoint introdotti:

- `GET /`
- `GET /health`

### feature/docker

Commit principali:

    Add Docker ignore file
    Add Dockerfile for Flask application
    Add Docker Compose configuration

Modifiche introdotte:

- aggiunto `.dockerignore`
- aggiunto `Dockerfile`
- aggiunto `docker-compose.yml`
- configurata immagine Python 3.12 slim
- installate dipendenze nel container
- esposta porta 5000
- configurato avvio dell'applicazione nel container
- aggiunto Gunicorn come server WSGI per l'esecuzione containerizzata

File principali:

- `.dockerignore`
- `Dockerfile`
- `docker-compose.yml`

Risultato:

- immagine Docker costruibile
- applicazione eseguibile in container
- applicazione eseguibile tramite Docker Compose

### feature/local-pipeline

Commit principale:

    Add local pipeline and tests

Modifiche introdotte:

- aggiunti test automatici con Pytest
- aggiunto script `local-pipeline.ps1`
- esecuzione automatica dei test
- build automatica dell'immagine Docker
- avvio di un container temporaneo
- verifica automatica dell'endpoint `/health`
- cleanup finale del container

File principali:

- `tests/test_app.py`
- `local-pipeline.ps1`

Risultato:

- pipeline locale di validazione funzionante

### feature/aws-pipeline

Commit principale:

    Add AWS CodeBuild configuration

Modifiche introdotte:

- aggiunto `buildspec.yml`
- configurata build su AWS CodeBuild
- installazione dipendenze in fase di build
- esecuzione test in pipeline AWS
- preparazione artefatto per Elastic Beanstalk
- configurata pipeline GitHub -> CodePipeline -> CodeBuild -> Elastic Beanstalk

File principali:

- `buildspec.yml`

Risultato:

- pipeline AWS funzionante
- deploy automatico su Elastic Beanstalk funzionante

## Fix e problemi risolti

Albero delle correzioni:

    fixes
    ├── Fix test imports for AWS CodeBuild
    ├── Fix Elastic Beanstalk access through HTTP
    └── Fix missing templates in Docker image

### Fix test imports for AWS CodeBuild

Problema:

Durante l'esecuzione dei test in AWS CodeBuild, Pytest non riusciva a importare correttamente `app.py`.

Soluzione:

Nel file `tests/test_app.py` è stato aggiunto il path della root del progetto:

    PROJECT_ROOT = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(PROJECT_ROOT))

Risultato:

- test funzionanti sia in locale sia su AWS CodeBuild

### Fix Elastic Beanstalk access through HTTP

Problema:

Il dominio Elastic Beanstalk risolveva correttamente, ma l'applicazione non era raggiungibile dal browser.

Soluzione:

È stato controllato il Security Group associato all'istanza EC2 ed è stata verificata l'apertura della porta HTTP 80.

Risultato:

- applicazione raggiungibile via HTTP
- dashboard e API accessibili online

### Fix missing templates in Docker image

Problema:

La dashboard funzionava con `python app.py`, ma in Docker restituiva `Internal Server Error`.

I log del container mostravano:

    jinja2.exceptions.TemplateNotFound: index.html

Causa:

La cartella `templates` non era presente dentro l'immagine Docker.

Soluzione:

Nel `Dockerfile` è stata aggiunta la riga:

    COPY templates ./templates

Risultato:

- dashboard HTML funzionante anche dentro Docker
- container locale funzionante con `local-deploy.ps1`
- pipeline locale funzionante con `local-pipeline.ps1`

## Stato finale

    stato finale
    ├── Flask app funzionante
    ├── dashboard HTML funzionante
    ├── API REST funzionante
    ├── health check funzionante
    ├── test automatici funzionanti
    ├── Docker funzionante
    ├── pipeline locale funzionante
    ├── deploy locale persistente funzionante
    ├── pipeline AWS funzionante
    └── deploy Elastic Beanstalk funzionante
