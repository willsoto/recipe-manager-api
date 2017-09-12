# Recipe Manager API

## Getting Started

### Cloning

```sh
git clone --recursive git@github.com:willsoto/recipe-manager-api.git
```

### Pre-commit Hooks

We use [pre-commit](http://pre-commit.com/) for our pre-commit hooks.
Please follow the [installation instructions](http://pre-commit.com/#install) for getting started.

### Docker

[Docker](https://www.docker.com/) is being used to manage this project, this README assumes you already have Docker installed.

### Prerequisites

Copy `.env.example` to `.env` and fill out any missing fields.

### Install

```sh
docker-compose up -d [--build]
```

### Container commands

The following commands are to be run in the context of a container. You can accomplish this one of two ways.

1. By using docker-compose to run the command directly, `docker-compose run <container> <command>`
2. By using docker-compose to launch a `bash` shell within a container, and then running the command(s) in the shell.
```sh
docker-compose run --rm <container> bash
# a bash shell gets launched within that container
<command>
```

### To initialize the database schema

```sh
docker-compose run --rm web flask create
```

### To update the database schema

```sh
docker-compose run --rm web alembic upgrade head
```

### Interacting with the database

Using [pgcli](http://pgcli.com/) you can run the following (using default dev environment variables):

```sh
pgcli --host localhost --port 5432 --user postgres recipe_manager_dev
```

### Logging in with Google

1. Go to the [Google Developer's Console](https://console.developers.google.com/)
2. Create a project
3. Create credentials for an "OAuth client ID"
4. Add the following URLs
    * *Authorized JavaScript origins*
        * `https://recipe-manager.dev`
    * *Authorized Redirect URIs*
        * `https://recipe-manager.dev/auth/google/callback`
5. Go to `https://recipe-manager.dev/auth/google` and authorize the application

### Running Celery

Open a shell in the `web` container:

```sh
docker-compose run --rm web bash
```

and then run:

```sh
celery -A recipe_manager.tasks.celery worker --loglevel=info
```
