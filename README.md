# Project Setup Guide

## Running the Backend

1. **Create a Free Redis Database**
   - Sign up for a free Redis database at [Redis Try Free](https://redis.io/try-free/).

2. **Setup and Run Backend**
   ```bash
   cd backend
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   python seeder.py
   python app.py
   ```

3. **Configuration**
   - Create a .env file in the backend directory with the following content:
    ```dotenv
    CACHE_REDIS_HOST=redis-....c252.ap-southeast-1-1.ec2.redns.redis-cloud.com
    CACHE_REDIS_PORT=149...
    CACHE_REDIS_PASSWORD=aBpUN...
    CACHE_REDIS_DB=0
    CACHE_DEFAULT_TIMEOUT=300
    JWT_SECRET_KEY=your_jwt_secret_key
    ```

## Running the Frontend
```bash
cd frontend
npm install
npm run dev
```