 **Let me help you find your way.**

PARTH is a user-friendly government service navigator that helps citizens discover relevant government services, understand general eligibility and required documents, and navigate toward official government portals.

## 🌐 Live Demo

**Live Website:** https://parth-government-service-navigator.onrender.com/login

> **Note:** PARTH is an independent project and is **not an official government website**. Always verify important information and application details on the relevant official government portal.

## ✨ Features

- 🔐 Login and Signup
- 🤖 Rule-based government-service chatbot
- 🔎 Find and explore government services
- 📄 Service information, eligibility, documents, and process guidance
- 📋 My Applications / saved services
- 📞 Contact Us
- 📱 Responsive and clean user interface
- 🔒 Password hashing for user accounts
- ☁️ Deployed online using Render

## 🏛️ Available Services

The current prototype includes guidance for:

1. Income Certificate
2. Caste Certificate
3. Scholarships
4. Birth Certificate
5. Government Pension
6. Aadhaar Services

## 🛠️ Technology Stack

- **Backend:** Python + Flask
- **Frontend:** HTML, CSS, JavaScript
- **Database:** SQLite (prototype)
- **Server:** Gunicorn
- **Deployment:** Render
- **Version Control:** GitHub

## 🚀 Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/raghawkoutu/PARTH-Government-Service-Navigator.git
cd PARTH-Government-Service-Navigator
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the application

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

## ☁️ Deployment

PARTH is configured for deployment on Render.

**Build command:**

```text
pip install -r requirements.txt
```

**Start command:**

```text
gunicorn app:app
```

The production deployment uses a `SECRET_KEY` environment variable.

## ⚠️ Current Prototype Limitations

For a larger production deployment, the project should be improved with:

- PostgreSQL or another persistent production database
- CSRF protection
- Rate limiting
- Account recovery
- Email verification when appropriate
- Monitoring and error tracking
- Privacy Policy and Terms of Service
- Regular verification of government-service information and official URLs
- Production-grade authentication and session management

## 🔐 Privacy & Security

Do not commit passwords, API keys, secret keys, `.env` files, or database files containing personal information to GitHub.

The project includes a `.gitignore` intended to prevent local database and secret files from being committed.

## ⚖️ Disclaimer

PARTH is an independent educational/project application. It does not represent, speak for, or operate on behalf of any government department or agency.

Information shown by PARTH is intended for general navigation and guidance. Users should always confirm eligibility, required documents, fees, deadlines, and application procedures on the relevant official government website before taking action.

## 📩 Contact

**Email:** mangaldaku2006@gmail.com

## 📄 License

This project is currently provided as an educational/project prototype.
