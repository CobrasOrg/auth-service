# Authentication Service

A modern, secure authentication service built with FastAPI, MongoDB, and complete observability stack (Prometheus & Grafana).

## Features

- 🔐 Secure user authentication and authorization
- 📨 Email verification and password reset functionality
- 🗄️ MongoDB integration for data persistence
- 📊 Built-in monitoring with Prometheus and Grafana
- 🚀 Fast and async API endpoints
- 📝 API documentation (Swagger/OpenAPI)
- 🐳 Docker and Docker Compose support

## Prerequisites

- Python 3.10+
- Docker and Docker Compose
- MongoDB (if running locally)

## Local Development Setup

### 1. Clone the repository

```bash
git clone https://github.com/CobrasOrg/auth-service
cd auth-service
```

### 2. Set up a virtual environment

```bash
python -m venv venv
# On Windows
.\venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Variables

Create a `.env` file in the root directory with the following variables (adjust as needed):

```env
DEBUG=True
API_V1_STR=/api/v1
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=authDB
TEST_DB_NAME=authDB_test
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
RESET_TOKEN_EXPIRE_MINUTES=15
GMAIL_USER=email@example.com
GMAIL_PASS=gmail_app_password
FRONTEND_URL=http://localhost:5173
EMAIL_FROM_NAME=account_name
EMAIL_TEMPLATES_DIR=app/templates
RESET_PASSWORD_URL=reset-password
```

### 5. Run the application locally

```bash
uvicorn main:app --reload
```

The API will be available at:
- Main API: `http://localhost:8000`
- API Documentation (Swagger UI): `http://localhost:8000/api/v1/docs`
- API Documentation (ReDoc): `http://localhost:8000/api/v1/redoc`

## Docker Deployment

To run the entire stack (API, MongoDB, Prometheus, and Grafana):

```bash
docker-compose up -d
```

Configure DB env:

```env
MONGODB_URL=mongodb://localhost:27017
```

This will start:
- Authentication Service: `http://localhost:8000`
- MongoDB: `mongodb://localhost:27017`
- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3000`

## API Endpoints

### Authentication
- `POST /api/v1/auth/login`  
  **Login with email and password**  
  Authenticates a user and returns an access token.

- `POST /api/v1/auth/logout`  
  **Logout**  
  Invalidates the current access token.

- `POST /api/v1/auth/register/owner`  
  **Register a new pet owner**  
  Creates an account for a new owner user.

- `POST /api/v1/auth/register/clinic`  
  **Register a new clinic**  
  Creates an account for a new clinic user.

- `POST /api/v1/auth/forgot-password`  
  **Request password reset**  
  Sends a password reset link to the user’s email.

- `POST /api/v1/auth/reset-password`  
  **Reset password**  
  Resets a user’s password using a valid token.

- `PUT /api/v1/auth/change-password`  
  **Change password**  
  Allows an authenticated user to change their password.

- `POST /api/v1/auth/verify-token`  
  **Verify access token**  
  Validates a token and returns user data if valid.


### User Management
- `GET /api/v1/user/profile`  
  **Get current user's profile**  
  Returns profile info of the currently authenticated user.

- `PATCH /api/v1/user/profile`  
  **Update current user's profile**  
  Partially updates profile fields (e.g., name, locality).

- `DELETE /api/v1/user/account`  
  **Delete user account**  
  Permanently deletes the user’s account.

## Monitoring

The Grafana dashboard configuration used in this project was adapted from [Kludex/fastapi-prometheus-grafana](https://github.com/Kludex/fastapi-prometheus-grafana).


The service includes a complete observability stack:

- **Prometheus**: Collects metrics from the FastAPI application
  - Access: `http://localhost:9090`

- **Grafana**: Visualizes the metrics with pre-configured dashboards
  - Access: `http://localhost:3000`
  - Default credentials: admin/admin

## Project Structure

```
auth-service/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── auth.py
│   │       │   ├── debug.py
│   │       │   └── user.py
│   ├── core/
│   │   ├── auth.py
│   │   ├── config.py
│   │   ├── security.py
│   │   └── tokens.py
│   ├── db/
│   │   ├── database.py
│   │   ├── mongo.py
│   │   └── mongo_token_store.py
│   ├── schemas/
│   │   ├── auth.py
│   │   └── user.py
│   ├── services/
│   │   ├── auth_service.py
│   │   └── user_service.py
│   └── templates/
│       ├── password_reset.html
│       └── password_reset.txt
├── grafana/
│   └── provisioning/
│       ├── dashboards/
│       └── datasources/
├── prometheus/
│   └── prometheus.yml
├── docker-compose.yaml
├── Dockerfile
├── main.py
└── requirements.txt
```

## Security Features

- Password hashing using bcrypt
- JWT tokens for authentication
- Token blacklisting for logout
- Email verification
- Password reset functionality
- Environment-based configuration