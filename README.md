# TxT Sink API
## Local Development Setup Instructions 

### 0. Prerequisites
You need the prerequisites below installed on your machine.

- Ubuntu (tested on windows wsl2: 24.04.1 LTS )
- Python v3.12.10
- Docker v27.4.1
- Make v4.3
- Poetry v1.8.5

### 1. Create a virtual environment
- Create a virtual environment using python and activate it for poetry to install the dependencies.

```bash
python3 -m venv .venv-txt-sink-api
```

- Activate the virtual environment, for every new terminal session you need to activate the virtual environment. You can deactivate the virtual environment by running `deactivate` command.

```bash
source .venv-txt-sink-api/bin/activate
```



### 2. Install dependencies
Now you can install the dependencies by running the command below.

```bash
make install
```

### 3. Update environment variables
Copy `settings.dev.py` and update the local environment variables with your own values

```bash
mkdir -p local
cp src/core/settings/templates/settings.dev.py ./local/settings.dev.py
```

### 4. Start the dependency containers
We use `docker compose` to start the dependency containers. Our dependencies are `mysql` (database) and `minio` (local s3 emulation). 
```bash
make dev-up
```

### 5. Apply the migrations

```bash
make migrate
```

### 6. Create a superuser

```bash
make superuser
```

### 7. Start development

```bash
make runserver
```