### Python Docker Runner

### Stage 1 
FROM python:3.12-slim as builder

# Create App Directory
WORKDIR /script

# Set API Token
ARG API_TOKEN

# Install Build Dependencies
RUN true \
    && apt-get update \
    && apt-get install -y \
    git

# Copy Git Repo
RUN git clone https://${API_TOKEN}@git.redclay.k12.de.us/Philip.Smallwood/RC-Renaissance .

# Checkout Repo
RUN git checkout docker 

# Create Python Virtualenv
RUN python -m venv venv

# Configure Python Virtualenv
RUN . venv/bin/activate && \
    pip install --no-cache-dir \
        -r ./requirements.txt \
        --extra-index-url https://${API_TOKEN}@git.redclay.k12.de.us/api/packages/Philip.Smallwood/pypi/simple

### Stage 2
FROM python:3.12-slim

# Install Run Dependencies
RUN true \
    && apt-get update \
    && apt-get install -y \
    cron \
    tzdata

# Upgrade Pip
RUN pip3 install --upgrade pip

# Set Time Zone
ENV TZ=America/New_York
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Copy App to Directory
WORKDIR /script

COPY --from=builder /script/ /script/

# Create Config Directory
WORKDIR /config_files

RUN mkdir -p ./key_file

RUN mkdir -p ./env_file

RUN mkdir -p ./export_files

# Create Cron Job Directory
RUN mkdir -p /etc/cron.d

# Set Cron Schedule
RUN echo "25 6 * * * root /script/venv/bin/python /script/ren_daily_updater/ren_main.py" >> /etc/crontab

ENTRYPOINT [ "cron", "-f" ]
