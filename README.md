# Healthcare Chatbot using Langchain Framework

## 1. Install Poetry
https://python-poetry.org/docs/#installation

## 2. Install dependencies
```sh
poetry install --no-root
```
If you use Conda or any different package manager, install all dependencies listing in pyproject.toml file

## 3. Create .env file based on the .env.example file, and enter the necessary configurations

## 4. Run web server
```sh
make run
```
or
```sh
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```
or
```sh
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

## 5. Access API through URL: http://localhost:8080/docs#/

# How to run LLM model in local environment

## 1. Install Ollama
https://ollama.com/download


## 2. Install Llama3.1 (8B parameters) (tool calling supported)
```sh
ollama run llama3.1
```
or
```sh
ollama pull llama3.1
```