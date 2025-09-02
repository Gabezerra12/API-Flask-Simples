# API Básica com Flask

Projeto de exemplo de uma API REST em Flask (CRUD de usuários) — armazenamento em memória.

## Requisitos
- Python 3.x
- Flask
Instalar:
    pip install flask

## Como executar
1. Abra o terminal na pasta do projeto:
    cd "c:\Users\gamer\Desktop\API FLASK atividade"
2. Execute:
    python app.py
3. Verifique no terminal a linha: *Running on http://127.0.0.1:5000*

Observação: dados são mantidos em memória (variável `usuarios`). Reiniciar o servidor apaga os dados.

## Rotas / Endpoints
Base: http://127.0.0.1:5000

- GET /  
  - Descrição: rota raiz para verificar se a API está ativa  
  - Resposta: 200
  - Exemplo: {"mensagem":"API ativa. Use /users para operar."}

- POST /users  
  - Cria usuário. Body JSON obrigatório: `{"nome":"...", "email":"..."}`
  - Validações: nome não vazio; email básico (contém @); email único
  - Respostas: 201 (criado) / 400 (JSON inválido ou validação falhou)

- GET /users  
  - Retorna lista (array) de usuários. 200

- GET /users/<id>  
  - Retorna usuário por id. 200 / 404 (não encontrado)

- PUT /users/<id>  
  - Atualiza `nome` e/ou `email`. Enviar JSON com pelo menos um dos campos.
  - Validações: mesmo comportamento de criação (email único entre usuários)
  - Respostas: 200 / 400 / 404

- DELETE /users/<id>  
  - Remove usuário. Respostas: 200 / 404

Detalhes: a geração de id usa `id_atual` e é thread-safe (lock).

## Exemplos (Postman)
- Criar (POST /users)
  - URL: http://127.0.0.1:5000/users
  - Header: Content-Type: application/json
  - Body raw JSON:
    {"nome":"Gabriel","email":"gabriel@email.com"}

- Listar (GET /users)
  - URL: http://127.0.0.1:5000/users

- Buscar (GET /users/1)
  - URL: http://127.0.0.1:5000/users/1

- Atualizar (PUT /users/1)
  - Body raw JSON (ex.:) {"nome":"Gabriel Silva"} ou {"email":"novo@email.com"}

- Deletar (DELETE /users/1)

## Exemplos rápidos (linha de comando)
PowerShell (Invoke-RestMethod):
    Invoke-RestMethod -Uri 'http://127.0.0.1:5000/users' -Method Post -ContentType 'application/json' -Body '{"nome":"Gabriel","email":"gabriel@email.com"}'
    Invoke-RestMethod -Uri 'http://127.0.0.1:5000/users' -Method Get

curl (Git Bash ou curl.exe):
    curl.exe -X POST "http://127.0.0.1:5000/users" -H "Content-Type: application/json" -d "{\"nome\":\"Gabriel\",\"email\":\"gabriel@email.com\"}"
    curl.exe "http://127.0.0.1:5000/users"

## Erros comuns
- 400: JSON inválido, campos faltando ou email em uso/ inválido.
- 404: rota inexistente ou usuário não encontrado.
- Se ver "Not Found" no navegador em `/`, use `/` ou `/users`. (A raiz já responde com mensagem JSON.)

## Próximos passos recomendados
- Adicionar testes com pytest + Flask test client.
- Persistir dados em um banco (SQLite/Postgres) para produção.
- Documentar exemplos de resposta no README ou usar ferramentas como Swagger/OpenAPI.