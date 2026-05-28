# TP 5 - Caixa de Mercado com Arquitetura em Camadas

Este projeto implementa um sistema de caixa de supermercado utilizando uma arquitetura em camadas bem definida, garantindo a separação de responsabilidades entre banco de dados, regras de negócio, controle e interface de usuário.

Nesta atualização foi adicionado web scraping dea lista de produtos para o csv, clientes populados por arquivo .json, criação de tabela e crud completo de clientes.

---

## Arquivos Executáveis (Pontos de Entrada)

### `main.py`
Este arquivo executa o sistema do caixa de supermercado (ponto de entrada para o operador). Ele popula o banco de dados com os valores do arquivo CSV e do aqruivo JSON na inicialização, gerencia o atendimento do cliente, registra as compras, realiza o fechamento do caixa e, ao encerrar, sincroniza e atualiza o arquivo CSV e JSON com os valores finais do banco de dados.

### `main_db.py`
Script utilitário responsável pela inicialização do banco de dados. Ele importa e executa a função `criar_db` contida em `data/gerenciamento_db.py`.

### `main_admin.py`
Interface de linha de comando para o administrador do sistema. Permite a realização de todas as ações de CRUD (Criação, Leitura, Atualização e Deleção) implementadas em `controller/produto_crud.py`, simulando o gerenciamento do estoque e disparando a sincronização com o CSV.

### `test.py`
Interface de linha de comando com controle para a realização de testes. Possui verificações para o funcionamento das camadas de repositório e serviço das tabelas de "Clientes" e "Produtos". Os testes podem ser encontrados na pasta `tests/`.

---

## Estrutura de Pastas e Camadas

### `classes/`
Contém 3 arquivos:
O arquivo `Modelo_base.py`, que define o modelo Base de classes usado nas classes existentes.
O arquivo `Produto.py`, que define a classe de entidade que representa o produto. Essa classe mapeia a estrutura dos elementos salvos no banco de dados, na tabela Produtos.
O arquivo `Cliente.py`, que define a classe de entidade que representa o cliente. Essa classe mapeia a estrutura dos elementos salvos no banco de dados, na tabela Clientes.

### `data/`
Contém o banco de dados SQLite (`mercado.db`), o arquivo de dados de produtos (`produtos.csv`), o arquivo de dados de clientes (`clientes.json`). Centraliza o arquivos `gerenciamento_db.py` e `web_scraping.py`.
O `gerenciamento_db.py` é responsável pelas seguintes rotinas essenciais:
* Criação do banco de dados (`criar_db`);
* Gerenciamento e verificação de conexões com o banco (`verificar_conexao_db`);
* Validação de integridade do arquivo CSV e JSON (`verificar_csv`, `verificar_json`);
* Carga inicial e alimentação do banco através do CSV e do JSON (`sincronizar_db_csv`, `sincronizar_db_json` e `alimentar_db`);
* Exportação e salvamento do banco de volta para o CSV e JSON (`salvar_produtos_para_csv` e `salvar_clientes_para_json`).
O `web_scraping.py` é repsonsável por:
* Realizar o scraping de produtos, preços e quantidades disponíveis de produtos em uma url. Esses dados ficam disponíveis ao banco de dados através do arquivo `produtos.csv`  (`realizar_scraping_produtos`).

> **Nota de Implementação:** No enunciado do TP4 foi solicitado que esta pasta se chamasse "Dados". Optei por manter o nome "Data" devido à extensão *Material Icon Theme* do VS Code, que customiza os ícones de pastas baseando-se em nomenclaturas padrão em inglês.

### `repository/`
Contém os arquivos `produto_repository.py` e `cliente_repository.py`. Esta camada é a única que acessa diretamente o banco de dados usando consultas/ORM. Nenhum tratamento de regra de negócio é feito aqui; quaisquer exceções capturadas no banco são propagadas para a camada de Serviço.

### `service/`
Contém os arquivos `produto_service.py` e `cliente_service.py`. É o "coração" das regras de negócio do sistema. Esta camada valida os campos do produto e cliente, checa consistência de dados e aplica validações de segurança. Define exceções customizadas do sistema e repassa os erros tratados para a camada de Controle.

### `controller/`
Contém os arquivos `produto_crud.py` e `cliente_crud.py`. Atua como intermediário entre a interface e o serviço. Ele orquestra as chamadas da camada de *Service* e padroniza os retornos em uma estrutura comum (indicando sucesso da operação, dados retornados, mensagens padrão ou erros ocorridos).

### `interface/`
Nesta pasta está o código de interface com o usuário (CLI), adaptado do TP3 para consumir a nova arquitetura de banco de dados. Ela reflete a tela que o funcionário interage no caixa de mercado. Contém:
* `caixa_mercado.py`: Tela principal de controle e fluxo das ações do caixa;
* `atendimento_cliente.py`: Funções de fluxo de compra de produtos para o cliente;
* `fechamento_caixa.py`: Emissão do fechamento e resumo financeiro do caixa;
* `gerenciamento_cliente.py`: Funções que envolvem e acionam o controller de clientes;
* `gerenciamento_produto.py`: Funções que envolvem e acionam o controller de produtos;
* `menus.py`: Renderização visual dos menus de opções no terminal;
* `registro_atendimento.py`: Apresentação e persistência de dados de atendimentos específicos;
* `tabelas.py`: Funções utilitárias para formatar e exibir dados em formato de tabelas no terminal.

### `tests/`
Centraliza os scripts de testes automatizados/manuais:
* `teste_repositorio_cliente.py` e `teste_repositorio_produto.py`: Testa isoladamente as operações da camada de repositório no banco de dados.
* `teste_servico_cliente.py` e `teste_servico_produto.py` (antigo `produto_cliente.py`): Testa o comportamento da camada de serviço (casos de sucesso e fluxos de erro);

### `utils/`
Contém módulos auxiliares com funções puras e repetitivas utilizadas em todo o projeto:
* `conexoes.py`: Funções para instanciar as conexões do banco, repositório, serviço e controle;
* `validador.py`: Funções de validação de entradas do usuário (ex: garantir que o input de quantidade seja um número válido);
* `geradores.py`: Captura da data atual do sistema.

Link do projeto no github: https://github.com/dev-pedr0/caixa-mercado