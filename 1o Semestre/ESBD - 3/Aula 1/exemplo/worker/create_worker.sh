#!/bin/bash

docker run -d --ipc=host --network=host flower_worker

# Criar a imagem do flower_worker:                      docker build --tag flower_worker .
# Matar (e remover) todos os flower_workers:            docker rm -f $(docker ps -a -q --filter "ancestor=flower_worker")