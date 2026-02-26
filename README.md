# FastAPI Full-Stack REST Demo

This repo is a full-stack app using the [FastAPI web framework](https://fastapi.tiangolo.com), MySQL for a database, and REST to interact with a simple users table. You may install MySQL natively or use the included Docker file to create a database in a containter. The `init-db.sql` defines a simple schema for use with the example.

![Screenshot](screenshot.png)

## Prerequesites

You just need to have Python 3.10+ installed.

## Usage

1. Create database credentials (specify your own **USERNAME**, **PASSWORD**, and **ROOT_PASSWORD**!)

    ```bash
    echo "MYSQL_HOST=localhost" > .env
    echo "MYSQL_DATABASE=ece140" >> .env
    echo "MYSQL_USER=USERNAME" >> .env
    echo "MYSQL_PASSWORD=PASSWORD" >> .env
    echo "MYSQL_ROOT_PASSWORD=ROOT_PASSWORD" >> .env
    ```

2. If you have Docker installed, run the following command to start up a MySQL server (ignore this step if you already have MySQL installed and modify the `.env` file to match your database credentials!). Run the command in a separate terminal window as it will lock up the window for logging.

    ```bash
    docker compose up --build -d
    ```

    **Note:** Just closing the terminal will not stop the database server. In order to stop it, you must issue the command `docker compose down` when you are finished.

3. Install `uv` (one-time)

    ```bash
    brew install uv
    ```

    If you don’t use Homebrew, see https://docs.astral.sh/uv/getting-started/ for alternatives.

4. Create a virtual environment and sync dependencies

    ```bash
    uv sync
    ```

5. Run the server (recommended: single worker)

    ```bash
    uv run server/main.py
    ```

## Persistence
- The server interacts with a MySQL database to persist user data.
- The database connection details are specified in the `.env` file.
- The `init-db.sql` file can be used to initialize the database schema if needed.
- The MySQL database will persist, even if the server is stopped because we volume mount the database data to the host machine in the `docker-compose.yml` file.