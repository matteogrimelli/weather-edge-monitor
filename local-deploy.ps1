# Interrompe lo script al primo errore PowerShell.
$ErrorActionPreference = "Stop"

# Nome dell'immagine Docker locale.
$imageName = "weather-edge-monitor"

# Nome del container persistente usato per testare l'app localmente.
$containerName = "weather-edge-monitor-local"

# Porta locale usata dal browser.
$hostPort = 5000

# Porta interna del container.
$containerPort = 5000

Write-Host "Starting local deployment..."

try {
    Write-Host "Step 1/5 - Running tests..."

    $venvPython = ".\venv\Scripts\python.exe"

    if (Test-Path $venvPython) {
        & $venvPython -m pytest
    }
    else {
        python -m pytest
    }

    if ($LASTEXITCODE -ne 0) {
        throw "Tests failed."
    }

    Write-Host "Step 2/5 - Building Docker image..."
    docker build -t $imageName .

    if ($LASTEXITCODE -ne 0) {
        throw "Docker build failed."
    }

    Write-Host "Step 3/5 - Removing previous local container if it exists..."

    $existingContainer = docker ps -a --filter "name=^/$containerName$" --format "{{.Names}}"

    if ($existingContainer -eq $containerName) {
        docker rm -f $containerName | Out-Null
    }

    Write-Host "Step 4/5 - Starting local container..."

    docker run -d --name $containerName -p "${hostPort}:${containerPort}" $imageName | Out-Null

    if ($LASTEXITCODE -ne 0) {
        throw "Docker container start failed."
    }

    Write-Host "Waiting for the application to start..."
    Start-Sleep -Seconds 5

    Write-Host "Step 5/5 - Checking health endpoint..."

    $healthUrl = "http://localhost:$hostPort/health"
    $response = Invoke-RestMethod -Uri $healthUrl

    if ($response.status -ne "ok") {
        throw "Health check failed. Expected status 'ok'."
    }

    Write-Host "Health check passed."
    Write-Host "Local deployment completed successfully."
    Write-Host "Application running at: http://localhost:$hostPort"
    Write-Host "Weather endpoint: http://localhost:$hostPort/api/weather?city=Modena"
}
catch {
    Write-Host "Local deployment failed."
    throw
}