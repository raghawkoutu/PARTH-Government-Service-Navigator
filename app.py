from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3
import os

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = "parth-secret-key"

DB = os.path.join(os.path.dirname(__file__), "parth.db")


SERVICES = [
    {
        "id": 1,
        "name": "Income Certificate",
        "category": "Certificates",
        "desc": "Apply for an income certificate and learn about required documents.",
        "docs": [
            "Identity proof",
            "Address proof",
            "Income-related documents"
        ],
        "steps": [
            "Check eligibility",
            "Prepare documents",
            "Open the official application portal",
            "Submit and track the application"
        ]
    },
    {
        "id": 2,
        "name": "Caste Certificate",
        "category": "Certificates",
        "desc": "Find guidance for applying for a caste certificate.",
        "docs": [
            "Identity proof",
            "Address proof",
            "Supporting caste document, if applicable"
        ],
        "steps": [
            "Check eligibility",
            "Prepare documents",
            "Apply through the official portal",
            "Track application status"
        ]
    },
    {
        "id": 3,
        "name": "Scholarship",
        "category": "Schemes & Benefits",
        "desc": "Find scholarship opportunities and application guidance.",
        "docs": [
            "Identity proof",
            "Previous marksheet",
            "Income certificate, if required",
            "Bank details"
        ],
        "steps": [
            "Check eligibility",
            "Find the applicable scholarship",
            "Prepare documents",
            "Apply on the official portal"
        ]
    },
    {
        "id": 4,
        "name": "Birth Certificate",
        "category": "Certificates",
        "desc": "Guidance for obtaining a birth certificate.",
        "docs": [
            "Identity/parent documents",
            "Birth registration details",
            "Address proof, if required"
        ],
        "steps": [
            "Locate the responsible authority",
            "Prepare documents",
            "Submit application",
            "Track the request"
        ]
    },
    {
        "id": 5,
        "name": "Government Pension",
        "category": "Schemes & Benefits",
        "desc": "Explore pension-related government services.",
        "docs": [
            "Identity proof",
            "Bank details",
            "Age/eligibility proof"
        ],
        "steps": [
            "Check eligibility",
            "Select the relevant pension",
            "Prepare documents",
            "Apply through the official portal"
        ]
    },
    {
        "id": 6,
        "name": "Aadhaar Services",
        "category": "Documents",
        "desc": "Find guidance for common Aadhaar-related services.",
        "docs": [
            "Aadhaar details or enrollment information",
            "Identity/address documents as applicable"
        ],
        "steps": [
            "Choose the required Aadhaar service",
            "Check requirements",
            "Use the official portal or authorized center"
        ]
    }
]


def get_db():
    connection = sqlite3.connect(DB)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():

    connection = get_db()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            mobile TEXT UNIQUE NOT NULL,
            email TEXT,
            password TEXT NOT NULL
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            service TEXT NOT NULL,
            status TEXT DEFAULT 'Guidance only',
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    connection.commit()
    connection.close()


# ---------------- HOME ----------------

@app.route("/")
def index():

    if "user_id" in session:
        return redirect(url_for("dashboard"))

    return render_template("login.html")


# ---------------- SIGNUP ----------------

@app.route("/signup", methods=["GET", "POST"])
def signup():

    error = None

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        mobile = request.form.get("mobile", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if not name or not mobile or not password:

            error = "Please fill in all required fields."

        else:

            try:

                connection = get_db()

                cursor = connection.execute(
                    """
                    INSERT INTO users
                    (name, mobile, email, password)
                    VALUES (?, ?, ?, ?)
                    """,
                    (name, mobile, email, password)
                )

                connection.commit()

                user_id = cursor.lastrowid

                connection.close()

                session["user_id"] = user_id
                session["name"] = name

                return redirect(url_for("dashboard"))

            except sqlite3.IntegrityError:

                error = "An account with this mobile number already exists."

    return render_template("signup.html", error=error)


# ---------------- LOGIN ----------------

@app.post("/login")
def login():

    mobile = request.form.get("mobile", "").strip()
    password = request.form.get("password", "")

    connection = get_db()

    user = connection.execute(
        """
        SELECT *
        FROM users
        WHERE mobile = ?
        AND password = ?
        """,
        (mobile, password)
    ).fetchone()

    connection.close()

    if not user:

        return render_template(
            "login.html",
            error="Invalid mobile number or password."
        )

    session["user_id"] = user["id"]
    session["name"] = user["name"]

    return redirect(url_for("dashboard"))


# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("index"))


# ---------------- DASHBOARD ----------------

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("index"))

    return render_template(
        "dashboard.html",
        name=session.get("name", "Citizen"),
        services=SERVICES
    )


# ---------------- SERVICES ----------------

@app.route("/services")
def services():

    if "user_id" not in session:
        return redirect(url_for("index"))

    return render_template(
        "services.html",
        services=SERVICES
    )


# ---------------- CONTACT ----------------

@app.route("/contact")
def contact():

    if "user_id" not in session:
        return redirect(url_for("index"))

    return render_template("contact.html")


# ---------------- SERVICE API ----------------

@app.route("/api/services")
def service_api():

    query = request.args.get("q", "").lower().strip()

    results = []

    for service in SERVICES:

        text = (
            service["name"]
            + " "
            + service["category"]
            + " "
            + service["desc"]
        ).lower()

        if not query or query in text:

            results.append(service)

    return jsonify(results)


# ---------------- CHATBOT ----------------

@app.post("/api/chat")
def chat():

    message = request.json.get("message", "").lower()

    service = None

    if any(word in message for word in [
        "scholarship",
        "student",
        "education"
    ]):

        service = SERVICES[2]

    elif "caste" in message:

        service = SERVICES[1]

    elif "income" in message:

        service = SERVICES[0]

    elif "birth" in message:

        service = SERVICES[3]

    elif "pension" in message:

        service = SERVICES[4]

    elif "aadhaar" in message or "aadhar" in message:

        service = SERVICES[5]

    else:

        return jsonify({
            "reply": """
I can help you find a government service.

Try telling me what you need, for example:

• Caste certificate
• Scholarship
• Income certificate
• Birth certificate
• Pension
• Aadhaar service
""",
            "service": None
        })

    return jsonify({
        "reply": (
            f"I think **{service['name']}** may be "
            "what you need. I can guide you through "
            "the documents and application process."
        ),
        "service": service
    })


# ---------------- SAVE SERVICE ----------------

@app.post("/api/save-application")
def save_application():

    if "user_id" not in session:

        return jsonify({
            "error": "Login required"
        }), 401

    service = request.json.get("service", "")

    connection = get_db()

    connection.execute(
        """
        INSERT INTO applications
        (user_id, service)
        VALUES (?, ?)
        """,
        (
            session["user_id"],
            service
        )
    )

    connection.commit()
    connection.close()

    return jsonify({
        "ok": True
    })


# ---------------- APPLICATIONS ----------------

@app.route("/applications")
def applications():

    if "user_id" not in session:
        return redirect(url_for("index"))

    connection = get_db()

    applications = connection.execute(
        """
        SELECT *
        FROM applications
        WHERE user_id = ?
        ORDER BY id DESC
        """,
        (session["user_id"],)
    ).fetchall()

    connection.close()

    return render_template(
        "applications.html",
        rows=applications
    )


# ---------------- START SERVER ----------------

if __name__ == "__main__":

    init_db()

    app.run(
        debug=True
    )