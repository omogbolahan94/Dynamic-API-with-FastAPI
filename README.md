# INTRODUCTION
This project is a backend API built with FastAPI that demonstrates how to design and implement RESTful endpoints with seamless integration to a PostgreSQL database using SQLAlchemy ORM.

The API provides structured endpoints for creating, reading, updating, and deleting data, while maintaining best practices such as modular design, environment-based configuration, and clear documentation.

As part of the development workflow, all endpoints have been tested against a live PostgreSQL instance to ensure correctness and reliability. This project serves as a foundation for building production-ready web services with Python, FastAPI, and PostgreSQL.

## Install FastAPI
`pip install fastapi[all]`

# Launching the Application Locally
* Activate the virtual environment: `source venv/scripts/activate`
* Start the app: `uvicorn app.main:app --reload`