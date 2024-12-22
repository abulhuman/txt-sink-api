TxT Sink API
============

Local Development Setup Instructions 

0. Prerequisites
---------------
You need the prerequisites below installed on your machine.

- Ubuntu (tested on windows wsl2: 24.04.1 LTS )
- Python v3.12.10
- Docker v27.4.1
- Make v4.3
- Poetry v1.8.5

1. Install dependencies
Now you can install the dependencies by running the command below.

```bash
make install
```

2. Copy settings.dev.py and update the local environment variables

```bash
mkdir -p local
cp src/core/settings/templates/settings.dev.py ./local/settings.dev.py
```

3. Start the dependency containers
We use `docker compose` to start the dependency containers. Our dependencies are `mysql` (database) and `minio` (local s3 emulation). 
You can start the containers by running the command below.
```bash
make dev-up
```

4. Apply the migrations

```bash
make migrate
```

5. Create a superuser

```bash
make superuser
```

6. Run the development server

```bash
make run
```