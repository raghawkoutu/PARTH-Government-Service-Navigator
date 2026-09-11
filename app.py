import os, sqlite3
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = os.environ.get("SECRET_KEY", "change-this-development-secret")
DATABASE = os.environ.get("DATABASE_PATH", "parth.db")

SERVICES = [
 {"id":"income","name":"Income Certificate","description":"Certificate used to prove annual family income for government services and benefits.","eligibility":"Residents who need official proof of income for an eligible government purpose.","documents":["Aadhaar/identity proof","Address proof","Income-related documents"],"process":"Check the applicable state portal, prepare documents, submit the application and track its status.","link":"https://services.india.gov.in/"},
 {"id":"caste","name":"Caste Certificate","description":"Official certificate used to establish caste/category status where applicable.","eligibility":"Eligible applicants who need a caste/category certificate under applicable rules.","documents":["Identity proof","Address proof","Supporting caste/category documents"],"process":"Use the applicable state or district government portal and follow its requirements.","link":"https://services.india.gov.in/"},
 {"id":"scholarship","name":"Scholarship","description":"Find government scholarship opportunities and application guidance.","eligibility":"Varies by scholarship, education level, category, income and other conditions.","documents":["Identity proof","Student/education documents","Bank details","Income/category documents if required"],"process":"Search the official scholarship portal, check the scheme requirements and submit before the deadline.","link":"https://scholarships.gov.in/"},
 {"id":"birth","name":"Birth Certificate","description":"Official record of a person's birth issued by the competent local authority.","eligibility":"Birth registration/certificate requests follow local registration rules.","documents":["Identity proof","Birth-related details/documents","Parent/guardian details where required"],"process":"Use the applicable municipal, state or official civil-registration service.","link":"https://services.india.gov.in/"},
 {"id":"pension","name":"Government Pension","description":"Guidance for finding eligible government pension and social-security schemes.","eligibility":"Varies by scheme, age, income, employment and other conditions.","documents":["Identity proof","Bank account details","Age/residence documents","Scheme-specific documents"],"process":"Identify the official scheme, verify eligibility, collect documents and apply through its designated channel.","link":"https://services.india.gov.in/"},
 {"id":"aadhaar","name":"Aadhaar Services","description":"Guidance for common Aadhaar-related services and official resources.","eligibility":"Requirements vary by the Aadhaar service requested.","documents":["Aadhaar details/number where applicable","Supporting documents where required"],"process":"Use official UIDAI resources to identify the correct service and requirements.","link":"https://uidai.gov.in/"}
]

def db():
    c=sqlite3.connect(DATABASE); c.row_factory=sqlite3.Row; return c

def init_db():
    c=db()
    c.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL,mobile TEXT NOT NULL,email TEXT NOT NULL UNIQUE,password TEXT NOT NULL)")
    c.execute("CREATE TABLE IF NOT EXISTS applications(id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER NOT NULL,service TEXT NOT NULL,status TEXT NOT NULL DEFAULT 'Guidance only',FOREIGN KEY(user_id) REFERENCES users(id))")
    c.commit(); c.close()

def required(f):
    @wraps(f)
    def w(*a,**k):
        if "user_id" not in session: return redirect(url_for("login"))
        return f(*a,**k)
    return w

def service(sid): return next((s for s in SERVICES if s["id"]==sid),None)

@app.route("/")
def index(): return redirect(url_for("dashboard" if session.get("user_id") else "login"))

@app.route("/signup",methods=["GET","POST"])
def signup():
    if request.method=="POST":
        name=request.form.get("name","").strip(); mobile=request.form.get("mobile","").strip()
        email=request.form.get("email","").strip().lower(); password=request.form.get("password","")
        if not all([name,mobile,email,password]): flash("Please fill in all fields.","error"); return render_template("signup.html")
        if len(password)<6: flash("Password must be at least 6 characters.","error"); return render_template("signup.html")
        c=db()
        try:
            c.execute("INSERT INTO users(name,mobile,email,password) VALUES(?,?,?,?)",(name,mobile,email,generate_password_hash(password))); c.commit()
            u=c.execute("SELECT id,name FROM users WHERE email=?",(email,)).fetchone()
        except sqlite3.IntegrityError:
            c.close(); flash("An account with this email already exists.","error"); return render_template("signup.html")
        c.close(); session["user_id"]=u["id"]; session["user_name"]=u["name"]; return redirect(url_for("dashboard"))
    return render_template("signup.html")

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        email=request.form.get("email","").strip().lower(); password=request.form.get("password","")
        c=db(); u=c.execute("SELECT * FROM users WHERE email=?",(email,)).fetchone(); c.close()
        if u and check_password_hash(u["password"],password):
            session["user_id"]=u["id"]; session["user_name"]=u["name"]; return redirect(url_for("dashboard"))
        flash("Invalid email or password.","error")
    return render_template("login.html")

@app.route("/logout")
def logout(): session.clear(); return redirect(url_for("login"))

@app.route("/dashboard")
@required
def dashboard(): return render_template("dashboard.html",user_name=session.get("user_name","User"))

@app.route("/services")
@required
def services(): return render_template("services.html",services=SERVICES)

@app.route("/applications")
@required
def applications():
    c=db(); rows=c.execute("SELECT id,service,status FROM applications WHERE user_id=? ORDER BY id DESC",(session["user_id"],)).fetchall(); c.close()
    return render_template("applications.html",applications=rows)

@app.route("/contact")
def contact(): return render_template("contact.html")

@app.route("/api/chat",methods=["POST"])
@required
def chat():
    m=(request.get_json(silent=True) or {}).get("message","").lower().strip()
    if not m: return jsonify(reply="Tell me which government service you need.")
    groups=[(["scholarship","student","education","college","school"],"scholarship"),(["caste","category","sc/st","obc"],"caste"),(["income","salary","earnings"],"income"),(["birth","born","dob"],"birth"),(["pension","senior citizen","old age"],"pension"),(["aadhaar","aadhar","uidai"],"aadhaar")]
    if any(x in m for x in ["hello","hi","hey"]): r="Hello! I'm PARTH. What government service are you looking for?"
    else:
        s=next((service(k) for words,k in groups if any(w in m for w in words)),None)
        r=(f"I found {s['name']}. {s['description']}") if s else "I can help with scholarships, income certificates, caste certificates, birth certificates, pensions and Aadhaar services. What do you need?"
    return jsonify(reply=r)

@app.route("/api/save-application",methods=["POST"])
@required
def save():
    sid=(request.get_json(silent=True) or {}).get("service_id"); s=service(sid)
    if not s: return jsonify(success=False,message="Service not found."),404
    c=db(); c.execute("INSERT INTO applications(user_id,service) VALUES(?,?)",(session["user_id"],s["name"])); c.commit(); c.close()
    return jsonify(success=True,message=f"{s['name']} saved to My Applications.")

init_db()
if __name__=="__main__": app.run(host="0.0.0.0",port=int(os.environ.get("PORT",5000)),debug=True)
