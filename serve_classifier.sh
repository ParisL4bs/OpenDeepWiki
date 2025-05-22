#!/bin/bash

# Serve indexer service using FastAPI

cd /app && python -m uvicorn indexer_service.server:app --host 0.0.0.0 --port 8002
