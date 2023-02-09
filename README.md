# FastAPI Javascript Starter

This repo is a full-stack app using the [FastAPI web framework](https://fastapi.tiangolo.com), MySQL for a database, and REST to interact with a simple users table. You may install MySQL natively or use the included Docker file to create a database in a containter. The `init-db.sql` defines a simple schema for use with the example.

## Prerequesites

You just need to have Python 3.7+ installed (3.10+ for the simplified typehinting).

## Usage

1. Create database credentials (**specify your own user and password!**)

    ```bash
    echo "MYSQL_HOST=localhost" > credentials.env
    echo "MYSQL_DATABASE=ece140" >> credentials.env
    echo "MYSQL_USER=" >> credentials.env
    echo "MYSQL_PASSWORD=" >> credentials.env
    ```

2. If you have Docker installed, run the following command to start up a MySQL server (please ignore this step if you already have MySQL installed!)

    ```bash
    docker compose up --build
    ```

3. Create a Python virtual environment

    ```bash
    python3 -m venv env
    ```

4. Start the virtual environment

    ```bash
    source env/bin/activate
    ```

5. Install dependencies

    ```bash
    pip install -U pip
    pip install -r requirements.txt
    ```

6. Run the server

    ```bash
    cd server
    python main.py
    ```

    or

    ```bash
    cd server
    uvicorn main:app --reload
    ```
