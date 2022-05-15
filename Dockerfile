FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

EXPOSE 8000/tcp

WORKDIR /picasso_parser

RUN apt-get -y update --no-install-recommends \
    && apt-get -y install --no-install-recommends \
    curl \
    && apt-get autoremove -y \
    && apt-get clean -y

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="${PATH}:/root/.local/bin"

COPY ./ ./
RUN poetry install

CMD ["poetry", "run",  "gunicorn", "config.asgi:application", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]