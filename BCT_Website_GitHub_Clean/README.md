# BCT Internal Platform

Internal web platform developed with Django as part of a university practical project in IT-Security.

## Overview

The platform centralizes internal communication and tools for sellers and team leaders. It includes modules for feedback, documents, team events, work safety information, news, partners, general information, and employee contact information.

## Features

- OTP-based login verification by email
- Role-based access control for sellers and team leaders
- Feedback and support system
- Document management
- Team event planning
- News and announcements
- Work safety information
- Team directory
- General information and partner overview

## Technologies

- Python
- Django
- SQLite
- HTML/CSS
- Git/GitHub

## Security Features

- One-Time Password (OTP) verification
- Role-based access restrictions
- Protected admin/teamleader areas
- Password reset and password change functions
- Restricted access to sensitive pages

## Local Setup

```bash
python -m venv .venv
# Windows:
.venv\\Scripts\\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Environment Variables

Create a `.env` file or configure environment variables based on `.env.example`.

## Note

Sensitive company data, real user data, database files, uploaded documents, and production configuration values were removed before publishing this repository.
