#!/bin/bash

echo "Starting ISP system deployment..."

# Install dependencies
pip install -r requirements.txt

# Create logs directory
mkdir -p logs

# Set permissions
chmod -R 777 logs

# Run database migration (if any)
python database/schema_init.py

# Start production server
gunicorn app:app -b 0.0.0.0:8000 --workers 4

echo "ISP System Running"