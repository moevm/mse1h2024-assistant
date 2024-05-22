#!/usr/bin/bash
sudo docker compose up -d ollama;
sudo docker exec -it ollama ollama pull llama3;
sudo docker compose up --build;
