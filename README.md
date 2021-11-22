# Project Structure

# Yarn

## Packages
- package.json
- yarn.lock

## Config
- webpack.config.js

## Workflow
- yarn
  - webpack
  - babel

## Output
- static/bundle.js

## Source
- src/index.jsx

```
yarn install
yarn run dev
```

# Python (Flask)

## Packages
- requirements.txt


## Config
- .flaskenv
- tilde.py
- app/__init__.py

## Source

- app/models.py
- app/routes.py
- app/templates/*

```
pip freeze > requirements.txt
pip install -r requirements.txt
```

# DB (SQLAlchemy)
- config.py
- migrations/*
- app.db


# Run

```
flask run
yarn run start
```

http://127.0.0.1:5000