# FastAPI Blog API

This project is a backend API built with FastAPI that demonstrates how to design and implement RESTful endpoints with secure authentication, database migrations, and modern deployment practices. It integrates seamlessly with a PostgreSQL database using SQLAlchemy ORM and Alembic for schema migrations.

The API now supports JWT-based user authentication and is production-ready with CORS enabled to allow resource sharing across different domains.

### 🚀 Features
* User Authentication: JWT token-based login and registration.
* CRUD Operations: Endpoints for creating, updating, deleting, and retrieving posts.
* PostgreSQL Integration: Database modeled with SQLAlchemy ORM.
* Alembic Migrations: Manage schema changes efficiently.
* CORS Support: Resource sharing enabled for cross-domain access.
* Deployment Ready: Configured for Render and Ubuntu servers.

### 📌 Endpoints
* POST /users/ → Register a new user
* POST /login/ → User login & JWT generation
* POST /posts/ → Create a new post
* GET /posts/{id} → Get a post by ID
* GET /posts/ → Get all posts
* PUT /posts/{id} → Update a post
* DELETE /posts/{id} → Delete a post

### 🛠 Installation & Setup
1. Clone Repository
```{bash}
git clone https://github.com/omogbolahan94/Dynamic-API-with-FastAPI.git
cd <project-folder>
```
2. Install Dependencies
```{bash}
pip install -r requirements.txt
```
3. Set Environment Variables

Create a .env file with:
```{ini}
DATABASE_HOSTNAME = your_db_hostname
DATABASE_PORT = your_db_port
DATABASE_DB_NAME = your_db_name
DATABASE_USER = your_db_username
DATABASE_PASSWORD = your_db_password

JWT_SECRET_KEY= your_secret_key
JWT_ALGORITHM = your_secret_algorithm
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = your_expiring_time
```

4. Run Database Migrations
```{bash}
alembic upgrade head
```
5. Launch Locally
```{bash}
uvicorn app.main:app --reload
```

### 🌍 Deployment

#### On Render
* Add a PostgreSQL instance from the Render dashboard.
* Set environment variables in the Render Dashboard.
* Use this Start Command: `uvicorn app.main:app --host 0.0.0.0 --port 10000`

#### On Ubuntu Server
I simulated production setup on WSL setting up Guvicorn to auto start application on reboot and NGINX.

### 📖 Tech Stack
* FastAPI
* PostgreSQL
* SQLAlchemy ORM
* Alembic
* JWT Authentication
* UvicorN
* NGINX
* Gunicorn