# Testing

Questo file descrive i test eseguiti per il progetto Weather Edge Monitor.

I test sono stati organizzati in tre livelli:

1. test automatici con Pytest
2. test locali con Docker
3. test su AWS dopo il deploy

## 1. Test automatici con Pytest

I test automatici sono definiti nel file:

```text
tests/test_app.py
```

Esecuzione:

```powershell
python -m pytest
```

Risultato atteso:

```text
5 passed
```

I test verificano:

- endpoint `/health`
- homepage `/`
- endpoint `/api/weather` senza parametro `city`
- endpoint `/api/weather?city=Modena`
- dashboard HTML con città inserita

Le chiamate verso Open-Meteo vengono simulate con `monkeypatch`, quindi i test non dipendono dalla rete esterna.

## 2. Test con virtual environment

Ambiente usato:

```text
Windows
PowerShell
Python virtual environment
Pytest
```

Attivazione del virtual environment:

```powershell
.\venv\Scripts\Activate.ps1
```

Installazione dipendenze:

```powershell
pip install -r requirements.txt
```

Esecuzione test:

```powershell
python -m pytest
```

Risultato ottenuto:

```text
5 passed
```

## 3. Test manuale con Python locale

Avvio applicazione:

```powershell
python app.py
```

URL testati da browser:

```text
http://localhost:5000/
http://localhost:5000/api/weather?city=Modena
http://localhost:5000/health
```

Risultato:

- la dashboard viene caricata correttamente
- il form permette di cercare una città
- l'API restituisce dati meteo in formato JSON
- l'endpoint `/health` restituisce lo stato dell'applicazione

Nota:

Il warning di Flask sul development server è normale in esecuzione locale. In Docker e su AWS l'applicazione viene eseguita tramite Gunicorn.

## 4. Test con Docker tramite local-deploy.ps1

Script utilizzato:

```powershell
.\local-deploy.ps1
```

Lo script esegue:

```text
test
build Docker
rimozione vecchio container locale
avvio nuovo container
health check
```

Risultato atteso:

```text
Health check passed.
Local deployment completed successfully.
Application running at: http://localhost:5000
```

Container usato:

```text
weather-edge-monitor-local
```

URL testati da browser:

```text
http://localhost:5000/
http://localhost:5000/api/weather?city=Modena
http://localhost:5000/health
```

Risultato:

- il container resta attivo
- la dashboard funziona da browser
- l'API meteo funziona da browser
- l'health check risponde correttamente

Comandi utili:

```powershell
docker ps
docker logs weather-edge-monitor-local
docker stop weather-edge-monitor-local
docker rm weather-edge-monitor-local
```

## 5. Test con pipeline locale

Script utilizzato:

```powershell
.\local-pipeline.ps1
```

Lo script esegue:

```text
test
build Docker
avvio container temporaneo
health check
cleanup
```

Risultato atteso:

```text
Health check passed.
Local pipeline completed successfully.
Cleaning up pipeline container...
```

Differenza rispetto a `local-deploy.ps1`:

- `local-pipeline.ps1` crea un container temporaneo e lo elimina alla fine
- `local-deploy.ps1` lascia il container attivo per test manuali da browser

## 6. Problema risolto durante i test Docker

Durante il test della dashboard tramite Docker si è verificato il seguente errore:

```text
Internal Server Error
```

Controllando i log del container:

```powershell
docker logs weather-edge-monitor-local
```

è stato individuato l'errore:

```text
jinja2.exceptions.TemplateNotFound: index.html
```

Causa:

La cartella `templates` non era copiata dentro l'immagine Docker.

Soluzione:

È stata aggiunta nel `Dockerfile` la riga:

```dockerfile
COPY templates ./templates
```

Dopo la ricostruzione dell'immagine, la dashboard ha funzionato correttamente anche nel container.

## 7. Test su AWS

Dopo il push su `main`, la pipeline AWS ha eseguito automaticamente:

```text
GitHub
AWS CodePipeline
AWS CodeBuild
AWS Elastic Beanstalk
```

URL testati online:

```text
http://weather-edge-monitor-env.eba-dzx73xvh.eu-west-1.elasticbeanstalk.com/
http://weather-edge-monitor-env.eba-dzx73xvh.eu-west-1.elasticbeanstalk.com/api/weather?city=Modena
http://weather-edge-monitor-env.eba-dzx73xvh.eu-west-1.elasticbeanstalk.com/health
```

Risultato:

- dashboard online funzionante
- API meteo online funzionante
- health check online funzionante
- deploy Elastic Beanstalk completato correttamente

## 8. Riepilogo

Risultato finale dei test:

```text
Pytest locale: OK
Python locale: OK
Docker local-deploy: OK
Docker local-pipeline: OK
AWS CodePipeline: OK
Elastic Beanstalk: OK
```