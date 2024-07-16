# Desafio Authentication - BackendBr

Link do desafio: https://github.com/backend-br/desafios/blob/master/authentication/PROBLEM.md


## Rodando o projeto
Este projeto foi construído com python, fastapi e sqlalchemy.
Copie o conteúdo do arquivo .env.template para um arquivo .env na raiz do projeto.

* Passo 1 (opcional)
    [Link para o pipx](https://pipx.pypa.io/stable/installation/#installing-pipx)

* Instalando o poetry (gerenciador de dependências)
    se instalou o pipx:

    ```
    pipx install poetry
    ```
    se não instalou o pipx:
    ```
    pip install poetry
    ```
* Instalando as dependências
    ```
    poetry install
    ```
* Ativando o ambiente virtual
    ```
    poetry shell
    ```
* Rodando as migrações do banco de dados (sqlite3)
    ```
    alembic upgrade head
    ```
* Rodando o projeto
    ```
    task run
    ```
* Rodando os testes:
    ```
    task test
    ```
    
