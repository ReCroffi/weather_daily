# 00 — Setup

## Postgres

Se não tiver rodando localmente:

```
docker run --name pg-clima -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres:16
```

Depois disso, o desenho da tabela `weather_daily` é seu — ver o contrato na fase 00 do roteiro.

## Ambiente Python com uv

Lembrete dos comandos (você quem roda, é a prática que interessa):

- `uv init` — inicializa o projeto nesta pasta (cria `pyproject.toml`)
- `uv add <pacote>` — adiciona e instala uma dependência, por exemplo:
  `uv add pandas requests sqlalchemy psycopg2-binary scikit-learn python-dotenv`
- `uv run <script>.py` — roda um script já dentro do ambiente do projeto, sem precisar ativar venv na mão
- `uv sync` — reinstala exatamente o que está travado no lockfile (útil depois de clonar/puxar)
- `uv remove <pacote>` — remove uma dependência

Não precisa criar venv manualmente (`uv venv`) — o `uv run`/`uv add` já cuidam disso sozinhos a partir do `uv init`.
