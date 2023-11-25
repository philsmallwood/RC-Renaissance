## 
FROM python:3.12-slim as builder

RUN pip3 install --upgrade pip

WORKDIR /script

ARG API_TOKEN

RUN true \
    && apt-get update && apt-get install -y git

RUN git clone https://${API_TOKEN}@git.redclay.k12.de.us/Philip.Smallwood/RC-Renaissance .

RUN git checkout docker 

RUN python -m venv venv

RUN . venv/bin/activate && \
    pip install --no-cache-dir \
        -r ./requirements.txt \
        --extra-index-url https://${API_TOKEN}@git.redclay.k12.de.us/api/packages/Philip.Smallwood/pypi/simple

FROM python:3.12-slim 

WORKDIR /script

COPY --from=builder /script/ /script/

WORKDIR /config_files

RUN mkdir -p ./key_file

RUN mkdir -p ./env_file

RUN mkdir -p ./export_files

CMD ["tail", "-f", "/dev/null"]