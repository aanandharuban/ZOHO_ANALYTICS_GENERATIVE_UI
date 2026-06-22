FROM python:3.13-slim AS base

WORKDIR /app

# 1. Inject the Deno runtime binary
COPY --from=denoland/deno:bin /deno /usr/local/bin/deno

COPY ./libs/sql_limit_enforcer/ ./libs/sql_limit_enforcer/
RUN pip install --no-cache-dir ./libs/sql_limit_enforcer/ && rm -rf /app/libs

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- FIX: Indentation-proof single-line Deno pre-caching ---
RUN python -c "import os, subprocess, fastmcp; [subprocess.run(['deno', 'cache', os.path.join(r, 'runner.js')]) for r, _, fs in os.walk(os.path.dirname(fastmcp.__file__)) if 'runner.js' in fs]"

COPY ./src/ ./src/

# stdio image
FROM base AS stdio
ENTRYPOINT ["python", "-m", "src.stdio"]

# http image
FROM base AS http
ENTRYPOINT ["python", "-m", "src.http_server"]