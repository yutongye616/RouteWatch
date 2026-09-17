# RouteWatch

RouteWatch is a Django-based transit operations dashboard built to showcase how a small city operations system could monitor public-road conditions, service risks, and operational issues using live public data.

## Problem it solves

Many public transit teams need a simple way to understand the operational picture across routes, incidents, and road conditions. This project models that workflow in a compact, interview-friendly application.

## Core idea

RouteWatch combines:

- a dashboard for route and incident visibility
- live NYC public-road data from the NYC Open Data crash feed
- a simple operational workflow for reviewing current conditions
- a clear monolithic architecture that is easy to explain in interviews

## Tech stack

- Python 3.9
- Django 4.2
- SQLite
- HTML / CSS
- Python standard library HTTP requests
- NYC Open Data API

## Features

- dashboard overview of operational activity
- live NYC road incident summary card
- route list driven by public data
- incident / maintenance management flow
- clean, readable UI for a portfolio demo

## Project structure

```text
RouteWatch/
├── manage.py
├── .env
├── .vscode/
├── operations/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── templates/
│   └── tests.py
├── routewatch/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── db.sqlite3
└── README.md
```

## Setup

1. Clone the repository.
2. Create and activate a virtual environment.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your local settings if needed.

5. Run migrations:

```bash
python manage.py migrate
```

6. Start the server:

```bash
python manage.py runserver 0.0.0.0:8000
```

7. Open the app in a browser:

```text
http://127.0.0.1:8000/
```

## Public data source

This project uses the NYC Open Data crash feed to show current roadway conditions in a portfolio-friendly way.

## Run tests

```bash
python manage.py test operations.tests
```

## Notes

This is designed as a lightweight portfolio project and is intentionally simple enough to explain clearly during interviews without requiring a complex microservices architecture.

## License

This project is for educational and portfolio use.
