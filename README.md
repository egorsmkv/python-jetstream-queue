# `python-jetstream-queue`

Queue based on NATS JetStream to show its abilities

## Install

### Install dependencies

```shell
uv venv --python 3.12

source .venv/bin/activate

uv pip install -r requirements.txt
uv pip install -r requirements-dev.txt
```

### NATS

Download NATS server:

```shell
mkdir nats-server && cd nats-server

wget https://github.com/nats-io/nats-server/releases/download/v2.10.17/nats-server-v2.10.17-linux-amd64.tar.gz && \
  tar xf nats-server-v2.10.17-linux-amd64.tar.gz && \
  mv nats-server-v2.10.17-linux-amd64/nats-server . && \
  rm -rf nats-server-v2.10.17-linux-amd64 && \
  rm nats-server-v2.10.17-linux-amd64.tar.gz
```

Run with JetStream:

```shell
./nats-server --debug --trace --jetstream --store_dir ./nats-data --user user1 --pass secret1 --addr 0.0.0.0 --port 4222
```

## Run

### Start the queue

```shell
python consume.py
```

### Send some data

```shell
python send_data.py
```

## Development

### Check/format the code

```shell
ruff check
ruff format
```
