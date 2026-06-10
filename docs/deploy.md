# Deploy

## Plano de Docker

Cada microsservico sera empacotado futuramente em sua propria imagem Docker, contendo a aplicacao FastAPI, suas dependencias Python e configuracoes necessarias para execucao isolada.

## Plano de Docker Compose

O Docker Compose sera usado para subir todos os componentes do projeto em ambiente local, conectando os microsservicos e o frontend em uma unica configuracao.

## Portas planejadas

- product-service: `8081`
- inventory-service: `8082`
- frontend: `3000`

## Plano de deploy futuro

O deploy futuro podera ser feito em uma plataforma com suporte a containers. A entrega final devera documentar o processo de build, configuracao das variaveis de ambiente, publicacao dos containers e validacao dos servicos em ambiente externo.
