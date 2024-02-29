FROM python:latest

RUN pip install poetry  
RUN mkdir -p /app  
COPY . /app

WORKDIR /app

ENV PATH="/app/.venv/bin:$PATH"

RUN poetry install
CMD ["poetry", "run", "python", "-m", "app.main"]
