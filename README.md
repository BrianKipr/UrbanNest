# UrbanNest

# Ecommerce Backend

## Overview

This is a backend application for an e-commerce platform built using Flask and SQLAlchemy.

## Setup

1. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2. Set environment variables in the `.env` file.

3. Initialize the database:
    ```bash
    flask db init
    flask db migrate -m "Initial migration"
    flask db upgrade
    ```

4. Run the application:
    ```bash
    flask run
    ```

## Endpoints

Refer to the `routes.py` file for available API endpoints and their usage.



