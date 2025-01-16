#!/bin/bash

uvicorn src.app.main:app --host 127.0.0.1 --port 8000 & python3 src/gradio/main.py