# Deploy

## Status

O deploy final ainda e um plano a realizar. Nao ha link publico publicado nesta fase.

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

## Plano de deploy futuro

O plano final e publicar os microsservicos conteinerizados em uma plataforma com suporte a Docker. Antes da publicacao, o pipeline devera executar testes, build das imagens e validacao dos endpoints principais.

Tambem sera necessario definir uma estrategia de persistencia para os bancos SQLite ou substituir por um banco gerenciado, conforme os requisitos do ambiente de deploy.
