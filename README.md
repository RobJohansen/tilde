# Project Structure


# Packages

## Yarn
- package.json
  - yarn.lock

```
yarn install
yarn run dev
```

## Python Flask
- requirements.txt

```
pip install -r requirements.txt
pip freeze > requirements.txt
```


# Workflow

## Input
- webpack.config.js

## Dependencies
- yarn
  - webpack
  - babel

## Output
- static/bundle.js


# App

# Config
- .flaskenv
- app/config/__init__.py

## React Templates
- src/index.jsx

```
yarn run start
```

## Flask App
- app/__init__.py
- app/models.py
- app/routes.py
- app/templates/*

```
flask run
```

## Flask Shell
- tilde.py

```
flask shell
```

# DB (SQLAlchemy)
- app/db/app.db
- migrations/*

```
flask db migrate
```


# Example

## Init
```
yarn install
pip install -r requirements.txt
```

## Run (Separate Terminals)
```
yarn run start
flask run
http://127.0.0.1:5000
```