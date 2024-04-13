#!/usr/bin/bash

sudo docker compose up -d --build;
sudo docker exec -it ollama ollama pull mistral
