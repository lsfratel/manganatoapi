FROM python:3.12-slim AS builder

ENV PDM_CHECK_UPDATE=false

WORKDIR /srv

RUN pip install -U pdm

COPY pyproject.toml pdm.lock README.md /srv

RUN pdm install --check --prod --no-editable

#------------------------------------------------------------------------------

FROM python:3.12-slim

WORKDIR /srv

COPY --from=builder /srv/.venv/ /srv/.venv

ENV PATH="/srv/.venv/bin:$PATH"

COPY manganatoapi /srv/manganatoapi

CMD ["gunicorn", "--access-logfile", "-", "--access-logformat", "%(t)s %(l)s %({x-forwarded-for}i)s %(r)s %(s)s %(b)s %(a)s", "--preload", "--threads", "8", "manganatoapi.wsgi"]
