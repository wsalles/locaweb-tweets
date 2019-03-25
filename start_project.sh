#/bin/bash

# Criando imagem:
docker build -t locaweb-tweets:1.0 .

# Criando serviço
docker service create\
 --replicas=1\
 -p 3333:3333\
 --name api-tweets locaweb-tweets:1.0
