# PARTH — Government Service Navigator

**Let me help you find your way.**

PARTH helps users discover government services, understand general eligibility and documents, and navigate to official portals.

## Features
- Login and signup (no OTP in this prototype)
- Rule-based government-service chatbot
- Service details
- My Applications / saved services
- Contact Us
- Responsive UI
- Secure password hashing

## Run locally
```bash
pip install -r requirements.txt
python app.py
```
Open `http://127.0.0.1:5000`.

## Render
Build command: `pip install -r requirements.txt`
Start command: `gunicorn app:app`

## Important
This prototype uses SQLite. Cloud-hosted SQLite may not provide permanent storage. For real public production use, migrate to PostgreSQL and add CSRF protection, rate limiting, account recovery, monitoring, privacy/terms pages, and verified official government URLs.

PARTH is an independent project, not an official government website. Always verify current information on the relevant official portal.

Contact: mangaldaku2006@gmail.com
