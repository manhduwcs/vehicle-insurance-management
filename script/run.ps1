# Exit on any error
$ErrorActionPreference = "Stop"

# Check if virtual environment exists
if (-Not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..."
    python -m venv venv
}

# Activate virtual environment
& .\venv\Scripts\activate

# Upgrade pip and install requirements
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Set port (default 8002)
param(
    [int]$PORT = 8002
)

Write-Host "Starting server on port $PORT ..."
python manage.py runserver $PORT