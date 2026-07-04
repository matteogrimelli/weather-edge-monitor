# Interrompe lo script al primo errore.
$ErrorActionPreference = "Stop"

# Nome dell'immagine Docker che verrà creata.
$imageName = "weather-edge-monitor"

# Nome del container usato solo dalla pipeline locale.
$containerName = "weather-edge-monitor-local-pipeline"

# Porta locale usata dalla pipeline.
# Uso 5050 per evitare conflitti con eventuali app già avviate su 5000.
$hostPort = 5050

Write-Host "Starting local CI/CD pipeline..."


try {
    Write-Host "Step 1/5 - Running tests..."

    # Usa il Python del virtual environment se esiste.
    # Altrimenti usa il Python disponibile nel sistema.
    $venvPython = ".\venv\Scripts\python.exe"

    if (Test-Path $venvPython) {
        & $venvPython -m pytest
    }
    else {
        python -m pytest
    }


    Write-Host "Step 2/5 - Building Docker image..."

    docker build -t $imageName .


    Write-Host "Step 3/5 - Removing old pipeline container if it exists..."

    $existingContainer = docker ps -a --filter "name=^/$containerName$" --format "{{.Names}}"

    if ($existingContainer -eq $containerName) {
        docker rm -f $containerName | Out-Null
    }


    Write-Host "Step 4/5 - Starting Docker container..."

    docker run -d --name $containerName -p "${hostPort}:5000" $imageName | Out-Null


    Write-Host "Waiting for the application to start..."
    Start-Sleep -Seconds 5


    Write-Host "Step 5/5 - Checking health endpoint..."

    $healthUrl = "http://localhost:$hostPort/health"
    $response = Invoke-RestMethod -Uri $healthUrl

    if ($response.status -ne "ok") {
        throw "Health check failed. Expected status 'ok'."
    }

    Write-Host "Health check passed."
    Write-Host "Local pipeline completed successfully."
}
finally {
    Write-Host "Cleaning up pipeline container..."

    $existingContainer = docker ps -a --filter "name=^/$containerName$" --format "{{.Names}}"

    if ($existingContainer -eq $containerName) {
        docker rm -f $containerName | Out-Null
    }
}