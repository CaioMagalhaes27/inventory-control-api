# Deploy

## Plano de Docker

Cada microsservico possui seu proprio `Dockerfile` usando `python:3.12-slim`. As imagens instalam as dependencias a partir do `requirements.txt` do respectivo servico e executam a aplicacao FastAPI com Uvicorn.

- `services/product-service/Dockerfile`: executa `uvicorn app.main:app --host 0.0.0.0 --port 8081`.
- `services/inventory-service/Dockerfile`: executa `uvicorn app.main:app --host 0.0.0.0 --port 8082`.

## Plano de Docker Compose

O Docker Compose sobe os microsservicos em containers separados e publica as portas planejadas no ambiente local.

```bash
docker compose build
docker compose up -d
```

Validacao local:

```bash
curl http://localhost:8081/api/products
curl http://localhost:8082/api/stock-items
```

Para encerrar o ambiente:

```bash
docker compose down
```

## Portas planejadas

- product-service: `8081`
- inventory-service: `8082`
- frontend: `3000`

## Plano de deploy futuro

O deploy futuro podera ser feito em uma plataforma com suporte a containers. O fluxo planejado e construir as imagens dos servicos, publicar em um registry, configurar variaveis de ambiente por ambiente e disponibilizar os containers em uma infraestrutura com suporte a Docker ou orquestracao equivalente.

Antes da publicacao, o pipeline devera executar testes automatizados, build das imagens e validacao dos endpoints de saude e das rotas principais.
