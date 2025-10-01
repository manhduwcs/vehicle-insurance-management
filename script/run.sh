#!/bin/bash
set -e  

if [ ! -d "venv" ]; then
    echo "Creating virtualenv..."
    python3 -m venv venv
fi

source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

python manage.py collectstatic --no-input

PORT=${1:-8002}
echo "Starting server on port $PORT ..."
python manage.py runserver $PORT