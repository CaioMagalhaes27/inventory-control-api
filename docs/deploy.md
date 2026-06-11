# Deploy

## Status

O frontend foi publicado no Netlify e os dois microsservicos FastAPI foram publicados no Render.

Links:

- Frontend: <https://inventory-control-frontend.netlify.app>
- Product Service: <https://inventory-control-api.onrender.com>
- Inventory Service: <https://inventory-stock-service.onrender.com>

O frontend publicado consome as APIs publicas do Render.

## Docker

Cada microsservico possui seu proprio `Dockerfile` com Python slim, instala `requirements.txt` e executa FastAPI com Uvicorn.

Servicos:

- product-service: `localhost:8081`
- inventory-service: `localhost:8082`

## Docker Compose

Build das imagens:

```bash
docker compose build
```

Subir os containers:

```bash
docker compose up -d
```

Encerrar:

```bash
docker compose down
```

Validacao local:

```bash
curl http://localhost:8081/api/products
curl http://localhost:8082/api/stock-items
```

## Persistencia em containers

Cada microsservico usa SQLite proprio:

- `product-service/data/products.db`
- `inventory-service/data/inventory.db`

No ambiente local com Docker Compose, os diretorios `data/` sao montados como volumes locais para preservar os bancos entre reinicios de containers.

Os arquivos `.db` sao ignorados pelo Git, pois representam dados locais de execucao.

Em producao, os bancos SQLite sao gerados no ambiente de cada servico no Render.

## Frontend

Para abrir o frontend estatico:

```bash
cd frontend
python -m http.server 3000
```

Acesse:

```text
http://localhost:3000
```

Funcionalidades principais:

- Dashboard.
- Cadastro de produtos.
- Cadastro de itens de estoque.
- Entrada e saida de estoque.
- Alertas de estoque baixo.
- Alertas de vencimento proximo.

Para uma execucao local integrada com proxy para as APIs, o projeto tambem possui `frontend/serve.py`.

## Observacoes sobre deploy

O Render Free pode demorar alguns segundos para responder apos inatividade, pois o servico pode entrar em repouso e precisar iniciar novamente na primeira requisicao.

Em evolucoes futuras, pode ser adotado um banco gerenciado ou uma estrategia de persistencia mais robusta, conforme os requisitos do ambiente de deploy.
