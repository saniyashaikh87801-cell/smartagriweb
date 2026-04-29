import hashlib
from flask import Blueprint, request, redirect, url_for, session, render_template_string
from database.db import query_db, execute_db

auth_bp = Blueprint("auth", __name__)


def hash_password(password: str) -> str:
    """Simple SHA-256 hash (use bcrypt in production)."""
    return hashlib.sha256(password.encode()).hexdigest()


# ── SIGN UP ──────────────────────────────────────────────────────────────────
@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    error = None
    if request.method == "POST":
        name     = request.form.get("name", "").strip()
        email    = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not name or not email or not password:
            error = "All fields are required."
        elif len(password) < 6:
            error = "Password must be at least 6 characters."
        else:
            existing = query_db("SELECT id FROM users WHERE email = ?", [email], one=True)
            if existing:
                error = "An account with this email already exists."
            else:
                execute_db(
                    "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                    [name, email, hash_password(password)]
                )
                session["user_email"] = email
                session["user_name"]  = name
                return redirect("/")

    return _render_signup(error)


# ── LOGIN ─────────────────────────────────────────────────────────────────────
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        email    = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = query_db(
            "SELECT * FROM users WHERE email = ? AND password = ?",
            [email, hash_password(password)],
            one=True
        )
        if user:
            session["user_email"] = user["email"]
            session["user_name"]  = user["name"]
            return redirect("/")
        else:
            error = "Invalid email or password."

    return _render_login(error)


# ── LOGOUT ────────────────────────────────────────────────────────────────────
@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# ── HTML RENDERERS ────────────────────────────────────────────────────────────
_BASE_STYLE = """
* {margin:0; padding:0; box-sizing:border-box; font-family:'Segoe UI', Arial, sans-serif;}
body {
    min-height:100vh;
    display:flex;
    justify-content:center;
    align-items:center;
    background: linear-gradient(135deg, #1a3a1f 0%, #2d6a35 50%, #3cb554 100%);
}
.auth-container { text-align:center; width:100%; padding:20px; }
.logo { color:#fff; margin-bottom:28px; }
.logo h1 { font-size:28px; font-weight:700; letter-spacing:-0.5px; }
.logo h1 em { color:#7ed497; font-style:normal; }
.logo p  { color:rgba(255,255,255,0.65); font-size:13px; margin-top:6px; }
.auth-card {
    background:#fff;
    padding:36px 32px;
    width:420px;
    max-width:100%;
    margin:0 auto;
    border-radius:16px;
    box-shadow:0 20px 60px rgba(0,0,0,0.25);
}
.auth-card h2 { color:#1a3a1f; margin-bottom:6px; font-size:22px; font-weight:700; }
.auth-card .subtitle { margin-bottom:24px; color:#6b8a70; font-size:13.5px; }
.auth-card input {
    width:100%; padding:11px 14px; margin-bottom:14px;
    border-radius:8px; border:1.5px solid #ddeee0;
    font-size:14px; color:#1a2e1d; outline:none;
    transition:border-color .2s;
}
.auth-card input:focus { border-color:#3cb554; }
.auth-card button {
    width:100%; padding:12px; background:#2e7d32;
    color:#fff; border:none; border-radius:8px;
    font-size:15px; font-weight:600; cursor:pointer;
    transition:background .2s, transform .15s;
    margin-top:4px;
}
.auth-card button:hover { background:#1b5e20; transform:translateY(-1px); }
.auth-link { margin-top:18px; font-size:13.5px; color:#6b8a70; }
.auth-link a { color:#2e7d32; text-decoration:none; font-weight:600; }
.auth-link a:hover { text-decoration:underline; }
.error-box {
    background:#fdecea; color:#c62828; border:1px solid #f5c6cb;
    border-radius:8px; padding:10px 14px; font-size:13px;
    margin-bottom:16px; text-align:left;
}
.divider { border:none; border-top:1px solid #ddeee0; margin:20px 0; }
"""


def _render_login(error=None):
    err_html = f'<div class="error-box">⚠ {error}</div>' if error else ""
    return render_template_string(f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>SmartAgriWeb | Login</title>
  <style>{_BASE_STYLE}</style>
</head>
<body>
<div class="auth-container">
  <div class="logo">
    <h1>🌱 Smart<em>Agri</em>Web</h1>
    <p>Intelligent Farming Dashboard</p>
  </div>
  <div class="auth-card">
    <h2>Welcome Back</h2>
    <p class="subtitle">Sign in to your SmartAgriWeb account</p>
    {err_html}
    <form method="POST" action="/login">
      <input type="email"    name="email"    placeholder="Email Address" required autocomplete="email"/>
      <input type="password" name="password" placeholder="Password"      required autocomplete="current-password"/>
      <button type="submit">Login</button>
    </form>
    <hr class="divider"/>
    <p class="auth-link">Don't have an account? <a href="/signup">Sign Up</a></p>
  </div>
</div>
</body>
</html>""")


def _render_signup(error=None):
    err_html = f'<div class="error-box">⚠ {error}</div>' if error else ""
    return render_template_string(f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>SmartAgriWeb | Sign Up</title>
  <style>{_BASE_STYLE}</style>
</head>
<body>
<div class="auth-container">
  <div class="logo">
    <h1>🌱 Smart<em>Agri</em>Web</h1>
    <p>Intelligent Farming Dashboard</p>
  </div>
  <div class="auth-card">
    <h2>Create Account</h2>
    <p class="subtitle">Register to use SmartAgriWeb</p>
    {err_html}
    <form method="POST" action="/signup">
      <input type="text"     name="name"     placeholder="Full Name"     required autocomplete="name"/>
      <input type="email"    name="email"    placeholder="Email Address" required autocomplete="email"/>
      <input type="password" name="password" placeholder="Password (min. 6 characters)" required autocomplete="new-password"/>
      <button type="submit">Sign Up</button>
    </form>
    <hr class="divider"/>
    <p class="auth-link">Already have an account? <a href="/login">Login</a></p>
  </div>
</div>
</body>
</html>""")