#!/bin/bash
set -e  

if [ ! -d "venv" ]; then
    echo "Creating virtualenv..."
    python3 -m venv venv
fi

if [[ "$OS" == "Windows_NT" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

pip install --upgrade pip
pip install -r requirements.txt

python manage.py collectstatic --no-input

PORT=${1:-8002}
echo "Starting server on port $PORT ..."
python manage.py runserver $PORT