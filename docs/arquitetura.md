# Arquitetura

## Microsservicos planejados

- product-service: cadastro, consulta e manutencao de produtos.
- inventory-service: controle de estoque, movimentacoes, validade, estoque minimo e alertas.

## Organizacao por Arquitetura Limpa

Cada microsservico sera organizado com separacao entre regras de negocio, casos de uso, detalhes tecnicos e interface da API.

## Camadas planejadas

- domain: entidades, regras de negocio e contratos centrais.
- application: casos de uso e orquestracao das regras de negocio.
- infrastructure: implementacoes externas, persistencia futura e integracoes.
- presentation: rotas FastAPI, schemas de entrada e saida e adaptadores HTTP.

## Principios SOLID planejados

- Single Responsibility Principle: cada classe ou modulo tera uma responsabilidade clara.
- Open/Closed Principle: regras serao estendidas sem alterar codigo ja validado sempre que possivel.
- Liskov Substitution Principle: contratos serao definidos para permitir substituicao segura de implementacoes.
- Interface Segregation Principle: interfaces pequenas serao preferidas para evitar dependencias desnecessarias.
- Dependency Inversion Principle: casos de uso dependerao de abstracoes, nao de detalhes de infraestrutura.

## Design Patterns planejados

- Repository: isolar o acesso a dados das regras de negocio.
- Factory: centralizar a criacao de objetos e dependencias.
- Strategy: permitir variacoes em regras de alerta, reposicao ou validade.
- Mapper: converter dados entre entidades, DTOs, schemas e modelos de infraestrutura.
