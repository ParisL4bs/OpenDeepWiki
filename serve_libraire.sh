#!/bin/bash

# Serve libraire service using FastAPI

cd /app && python -m uvicorn libraire_service.server:app --host 0.0.0.0 --port 8001
