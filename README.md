# Deploy on Vercel

Vercel loads the existing FastAPI app from the `app` entry in `pyproject.toml`.
Import this repository as a Vercel project and set these environment variables
for each deployment environment you use:

| Variable | Value |
| --- | --- |
| `DATABASE_URL` | A reachable PostgreSQL URL using the async driver, for example `postgresql+psycopg://user:password@host/database` |
| `OPENAI_ENDPOINT` | An HTTPS endpoint reachable from Vercel; a `localhost` URL will not work |
| `OPENAI_MODEL` | The model name at that endpoint |
| `OPENAI_API_KEY` | The endpoint's API key |

Apply the existing Alembic migration to that database from a machine with
database access before testing the deployment: `uv run alembic upgrade head`.
Use the same `DATABASE_URL` for the migration. Keep credentials in Vercel
environment variables, not in the repository.

Uploads are limited to 3 MiB. Vercel limits each function request and response
to 4.5 MB. The current `/list` and `/search` routes include document contents,
so responses containing several large documents can exceed that limit.
The app has no sign-in: anyone with its URL can upload and delete documents.
