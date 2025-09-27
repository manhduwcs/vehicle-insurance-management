#!/bin/bash
set -e  

if [ ! -d "venv" ]; then
    echo "Creating virtualenv..."
    python3 -m venv venv
fi

source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

python manage.py migrate

PORT=${1:-8000}
echo "Starting server on port $PORT ..."
python manage.py runserver 0.0.0.0:$PORT