# Testes

## Plano de TDD com pytest

O desenvolvimento seguira TDD nas regras principais de negocio. Antes de implementar cada comportamento, sera criado um teste automatizado com pytest descrevendo o resultado esperado. Em seguida, o codigo sera implementado de forma minima para passar no teste e depois refatorado mantendo a cobertura.

## Plano de BDD com Gherkin

Os fluxos principais do sistema serao descritos em linguagem Gherkin usando Behave ou pytest-bdd. Os cenarios devem representar comportamentos esperados do ponto de vista do usuario e servir como documentacao executavel da aplicacao.

## Cenarios previstos

- Cadastrar um produto com dados validos.
- Rejeitar cadastro de produto com campos obrigatorios ausentes.
- Registrar entrada de item no estoque.
- Registrar saida de item no estoque.
- Alertar quando o estoque ficar abaixo do minimo configurado.
- Alertar quando um produto estiver proximo do vencimento.
- Consultar produtos e itens disponiveis em estoque.
