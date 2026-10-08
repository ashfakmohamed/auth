# App Management API

<!-- profile-upgrade -->
[![Django CI](https://github.com/ashfakmohamed/django-app-management-api/actions/workflows/ci.yml/badge.svg)](https://github.com/ashfakmohamed/django-app-management-api/actions/workflows/ci.yml)

**Stack:** Python · Django · Django REST Framework · OpenAPI

A Django application where administrators publish apps and authenticated users upload task-completion screenshots. Administrators can review tasks and approve points.

## Security

- Django hashes account passwords.
- Users can only list and download their own task screenshots.
- Screenshot URLs are never exposed directly by the API.
- Only staff users can create or change apps and approve tasks.
- Task approval awards points once inside a database transaction.
- Secrets are loaded from the environment, and local media/databases are ignored by Git.

## Setup

1. Create and activate a Python virtual environment.
2. Install dependencies:

    python -m pip install -r requirements.txt

3. Configure the variables in .env.example. DJANGO_SECRET_KEY is required.
4. Initialize and run:

    python app_management/manage.py migrate
    python app_management/manage.py createsuperuser
    python app_management/manage.py runserver

5. Sign in at http://127.0.0.1:8000/accounts/login/.

API schema and interactive documentation:

- /api/schema/
- /api/docs/

For token-based API access, create a token with:

    python app_management/manage.py drf_create_token USERNAME

## Tests

    python app_management/manage.py check
    python app_management/manage.py test

## Engineering quality

- GitHub Actions runs Django checks and the automated test suite on every push.
- Runtime configuration is documented through `.env.example`; secrets are not committed.
- Local databases, uploaded media, caches, and virtual environments are excluded from version control.
- Security-sensitive behavior and authorization rules are documented above.