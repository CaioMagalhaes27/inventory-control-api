# Testes

## Estrategia

O projeto utiliza testes automatizados para validar os dois microsservicos e demonstrar TDD e BDD.

- Pytest valida regras de negocio e contratos HTTP usando FastAPI `TestClient`.
- Behave/Gherkin descreve cenarios de comportamento em linguagem de negocio.
- Os testes usam repositorios in-memory para isolamento e velocidade.
- O runtime da aplicacao usa SQLite com SQLAlchemy.

## Como rodar pytest

Product-service:

```bash
cd services/product-service
pytest
```

Inventory-service:

```bash
cd services/inventory-service
pytest
```

## Como rodar BDD com Behave/Gherkin

Product-service:

```bash
cd services/product-service
python -m behave
```

Inventory-service:

```bash
cd services/inventory-service
python -m behave
```

## Totais

Testes unitarios/API com pytest:

- product-service: 12 testes.
- inventory-service: 15 testes.
- Total: 27 testes.

Cenarios BDD com Behave/Gherkin:

- product-service: 6 cenarios.
- inventory-service: 6 cenarios.
- Total: 12 cenarios BDD.

## Cenarios principais do product-service

- Criar produto valido.
- Validar campos obrigatorios.
- Impedir SKU duplicado.
- Listar produtos.
- Buscar produto por id.
- Atualizar produto.
- Executar soft delete.
- Retornar erro para produto inexistente.

## Cenarios principais do inventory-service

- Criar item de estoque.
- Validar quantidade e estoque minimo.
- Registrar entrada.
- Registrar saida.
- Impedir saida com estoque insuficiente.
- Listar estoque baixo.
- Listar vencimento proximo.
- Recusar validade no passado.

## Relacao com TDD e BDD

TDD e demonstrado pelos testes pytest cobrindo os casos de uso antes da validacao final da implementacao. BDD e demonstrado pelos arquivos `.feature` em Gherkin, que descrevem fluxos esperados do ponto de vista do comportamento do sistema.
