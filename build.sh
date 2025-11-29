#!/bin/bash
# Build script for Vercel
# This script runs migrations and collects static files

cd src
python manage.py migrate --noinput || true
python manage.py collectstatic --noinput || true

