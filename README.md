# Inventory Control API

Sistema de controle de estoque, validade e reposicao para pequenos comercios.

## Descricao

O projeto tem como objetivo construir uma aplicacao web baseada em microsservicos para apoiar pequenos mercados, mercearias, restaurantes e lanchonetes no controle de produtos, estoque, validade e reposicao.

## Problema escolhido

Pequenos comercios perdem dinheiro por falta de controle sobre entradas e saidas de produtos, acompanhamento manual de estoque minimo e baixa visibilidade sobre itens proximos do vencimento.

## Solucao proposta

A solucao proposta e uma aplicacao web composta por microsservicos para cadastro de produtos, controle de itens em estoque, registro de movimentacoes, alertas de estoque baixo e alertas de vencimento proximo.

## Stack

- Python 3.11+
- FastAPI
- Pydantic
- Uvicorn
- Pytest

## Microsservicos

- `services/product-service`: cadastro e consulta de produtos. Porta `8081`.
- `services/inventory-service`: estoque, movimentacoes, estoque minimo e vencimento. Porta `8082`.

Cada servico segue arquitetura limpa em camadas:

```
app/
├── main.py
├── domain/
│   ├── entities/
│   ├── repositories/
│   └── exceptions/
├── application/
│   ├── use_cases/
│   ├── schemas/
│   ├── factories/
│   └── mappers/
├── infrastructure/
│   └── repositories/
└── presentation/
    ├── routers/
    └── exception_handlers/
```

## Como executar

Cada servico tem seu proprio `requirements.txt`. Em terminais separados:

```bash
# product-service
cd services/product-service
python -m venv .venv
source .venv/Scripts/activate     # Windows Git Bash
pip install -r requirements.txt
uvicorn app.main:app --port 8081 --reload
```

```bash
# inventory-service
cd services/inventory-service
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
uvicorn app.main:app --port 8082 --reload
```

Saude:
- `GET http://127.0.0.1:8081/health`
- `GET http://127.0.0.1:8082/health`

Documentacao OpenAPI: `/docs` em cada servico.

## Testes

```bash
cd services/product-service && pytest
cd services/inventory-service && pytest
```

Total atual: **27 testes passando** (12 em product-service, 15 em inventory-service).

## Conceitos demonstrados

- Clean Code e SOLID
- Arquitetura Limpa (domain / application / infrastructure / presentation)
- Design Patterns: Repository, Factory, Mapper, Strategy
- TDD (testes de API com FastAPI TestClient)
- Microsservicos isolados por dominio

## Documentacao adicional

- `docs/arquitetura.md` - arquitetura em camadas e patterns
- `docs/testes.md` - estrategia e cobertura de testes
- `docs/deploy.md` - notas de deploy
- `docs/entrega.md` - notas de entrega
