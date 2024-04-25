#!/usr/bin/bash
sudo docker compose up -d ollama;
sudo docker exec -it ollama ollama pull mistral;
sudo docker compose up -d --build;
