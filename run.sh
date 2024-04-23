#!/usr/bin/bash
sudo docker compose up -d ollama;
sudo docker exec -it ollama ollama pull mistral;
pip install docker;
# python3 setup.py;
sudo docker compose up -d --build;