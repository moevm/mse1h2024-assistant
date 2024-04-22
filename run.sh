#!/usr/bin/bash
sudo docker compose up -d ollama;
sudo docker exec -it ollama ollama pull mistral;
pip install docker;
sudo docker compose up -d --build;
python3 setup.py;
