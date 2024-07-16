# Create an Environment Variable in

```cmd
python -m venv venv
```

# Activate virtual env

```cmd
venv\Scripts\activate.bat
```

# Install FastAPI

```cmd
pip install fastapi
pip install uvicorn
```

# Generate requirements.txt

```cmd
pip freeze > requirements.txt
```

# Install from requirements.txt

```cmd
pip install -r requirements.txt.
```

# Create a main.py file in the root project.

```main.py
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}
```

# 1- Initializing my app

```cmd
uvicorn main:app --reload --port 5000
```

# 2- Initializing my app with host
## For accessing by IP host:

```cmd
uvicorn main:app --reload --port 5000 --host 0.0.0.0
```

# 3- Initializing my app with FastApi

```cmd
fastapi dev main.py --reload --port 5000
```
