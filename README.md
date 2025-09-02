# Youtube-IR-System

A FastAPI-based backend for searching and serving YouTube video metadata stored in Firestore.

---

## Prerequisites
Before you start, make sure you have the following installed:

- [Python 3.11+](https://www.python.org/downloads/) (if running locally without Docker)  
- [Docker](https://www.docker.com/get-started) (recommended)  
- A valid `serviceAccount.json` file for Firebase.


---

## Getting Started

### Add Firebase Credentials
Place your `serviceAccount.json` file in the **root of the project**. 

---


## Run Without Docker (Local Development)

If you want to run the app directly on your machine:

### Create a Virtual Environment

```bash
python -m venv env
source env/bin/activate   # On Linux/Mac
env\Scripts\activate      # On Windows
```

### Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Run the Server

```bash
uvicorn src.main:app --reload
```

### Test the API

Go to : [http://localhost:8000/docs](http://localhost:8000/docs)


## Run with Docker

### Build the Docker Image
Run this in the project root:

```bash
docker build -t youtube-ir-system .
````

### Start the Container

Run the container and expose it on port `8000`:

```bash
docker run -p 8000:8000 --name youtube-ir-system youtube-ir-system
```

### Explore the API

Open your browser at : [http://localhost:8000/docs](http://localhost:8000/docs)
You’ll see the **Swagger UI** to test all APIs. Logs will also show in your terminal.

---
