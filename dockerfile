## 
FROM python:3.12-slim

WORKDIR /script

ARG API_TOKEN

RUN true \
    && apt-get update && apt-get install -y \
    git

RUN git clone https://${API_TOKEN}@git.redclay.k12.de.us/Philip.Smallwood/RC-Renaissance .

RUN pip install --no-cache-dir \
    -r ./requirements.txt \
    --extra-index-url https://${API_TOKEN}@git.redclay.k12.de.us/api/packages/Philip.Smallwood/pypi/simple

RUN mkdir -p ./ren_daily_updater/config_files

CMD ["tail", "-f", "/dev/null"]