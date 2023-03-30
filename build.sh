#!/bin/bash

# Check if a virtual environment exists in the repository
if [[ -d "venv" ]]; then
  echo "Activating existing virtual environment..."
  source venv/bin/activate
else
  echo "Creating new virtual environment..."
  python3 -m venv venv
  source venv/bin/activate
  echo "Installing requirements..."
  pip install -r requirements_env.txt
fi

# Start the Django development server
echo "Starting server..."
python3 manage.py runserver
