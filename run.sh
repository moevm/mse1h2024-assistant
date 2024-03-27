#!/usr/bin/bash

sudo docker compose up -d;

sudo docker exec -it ollama ollama pull mistral
