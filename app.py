from flask import Flask, render_template_string, request, redirect, url_for, session 
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader


app = Flask(__name__)
app.secret_key = "pylaunch_secret"
# ================================
# BASE CSS 
# ================================
base_css = """
<style>
/* ================================
   Global Dark Theme
   ================================ */

body {
    margin: 0;
    font-family: 'Poppins', sans-serif;
    background: linear-gradient(135deg, #020617, #0f172a);
    color: #e5e7eb;
}

.container {
    display: flex;
    justify-content: center;
    padding: 60px 20px;
}

.card {
    background: rgba(15, 23, 42, 0.95);
    width: 850px;
    padding: 40px;
    border-radius: 22px;
    box-shadow: 0 40px 90px rgba(0, 0, 0, 0.8);
}
/* ================================
   SKILL GAP SPEEDOMETER
   ================================ */

.gauge-container {
    text-align: center;
    margin-top: 30px;
}

.gauge {
    width: 220px;
    height: 110px;
    background: #020617;
    border-radius: 220px 220px 0 0;
    position: relative;
    overflow: hidden;
    margin: auto;
}

.gauge-fill {
    width: 220px;
    height: 220px;
    background: linear-gradient(90deg, #ef4444, #facc15, #22c55e);
    position: absolute;
    top: 110px;
    left: 0;
    transform-origin: center top;
    transform: rotate(0deg);
    transition: transform 1s ease-in-out;
}

.gauge-cover {
    width: 180px;
    height: 90px;
    background: #0f172a;
    border-radius: 180px 180px 0 0;
    position: absolute;
    top: 20px;
    left: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 26px;
    font-weight: bold;
    color: #22d3ee;
}


/* ================================
   Headings
   ================================ */

h1, h2, h3 {
    color: #f8fafc;
}

/* ================================
   Text Content
   ================================ */

p {
    color: #cbd5f5;
    line-height: 1.8;
    font-size: 16.5px;   /* increased explanation size */
}

ul {
    margin-top: 10px;
}

li {
    margin-bottom: 18px;
    color: #e5e7eb;
}

/* Explanation / description text */
small {
    color: #cbd5f5;
    font-size: 16.5px;   /* increased explanation size */
    line-height: 1.8;
}

/* ================================
   Buttons 
   ================================ */

button {
    padding: 14px 24px;
    border-radius: 12px;
    border: none;
    background: linear-gradient(135deg, #6366f1, #22d3ee);
    color: #020617;
    font-weight: bold;
    cursor: pointer;
}

a {
    text-decoration: none;
}

/* ================================
   Link Color Fix 
   ================================ */

.card a,
.card a:visited {
    color: #f8fafc !important;   /* visible white links */
}

/* ================================
   Navigation
   ================================ */

.nav {
    display: flex;
    flex-wrap: wrap;              /* prevents overlapping */
    gap: 16px;                    /* spacing between buttons */
    justify-content: center;      /* neat centered layout */
    margin-top: 30px;
}
/* =========================================
   NAVIGATION ORDER 
   ========================================= */

.nav a[href="/applications"]     { order: 1; }
.nav a[href="/fresher"]          { order: 2; }
.nav a[href="/intermediate"]     { order: 3; }
.nav a[href="/advanced"]         { order: 4; }
.nav a[href="/experienced"]      { order: 5; }
.nav a[href="/skill-gap"]        { order: 6; }
.nav a[href="/resume-analyzer"]  { order: 7; }
</style>
"""
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from flask import send_file
import tempfile
import os

@app.route("/fresher-study-plan-pdf")
def fresher_study_plan_pdf():
    styles = getSampleStyleSheet()

    # Create temp PDF file (Windows-safe)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    temp_file.close()

    doc = SimpleDocTemplate(temp_file.name, pagesize=A4)
    content = []

    content.append(Paragraph("<b>Python Fresher Study Plan</b>", styles["Title"]))
    content.append(Paragraph(
        "Goal: Build strong Python fundamentals and become job-ready for entry-level roles.",
        styles["Normal"]
    ))

    study_plan = [
        "Week 1: Python basics, syntax, variables, input/output",
        "Week 2: Data types and collections (list, tuple, set, dictionary)",
        "Week 3: Control structures and functions",
        "Week 4: Strings and file handling",
        "Week 5: Exception handling, modules, packages",
        "Week 6: Object-Oriented Programming",
        "Week 7: Mini Project – Calculator",
        "Week 8: Mini Project – Student Management System"
    ]

    for item in study_plan:
        content.append(Paragraph(item, styles["Normal"]))

    content.append(Paragraph(
        "<br/>Tip: Consistency beats intensity. Code daily, even 30 minutes.",
        styles["Italic"]
    ))

    doc.build(content)

    return send_file(
        temp_file.name,
        as_attachment=True,
        download_name="Python_Fresher_Study_Plan.pdf"
    )



# -------------------------------
# LOGIN 
# -------------------------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["name"] = request.form["name"]
        return redirect("/levels")

    return render_template_string(base_css + """
    <div class="container">
      <div class="card" style="width:420px;">
        <h2>Welcome to PyLaunch!👋</h2>
        <form method="POST">
          <input name="name" placeholder="Your Name" required
            style="width:100%;padding:14px;margin-top:20px;border-radius:10px;border:none;">
          <button style="margin-top:20px;width:100%;">Enter</button>
        </form>
      </div>
    </div>
    """)

# -------------------------------
# LEVEL SELECT 
# -------------------------------
@app.route("/levels")
def levels():
    return render_template_string(base_css + """
    <meta http-equiv="refresh" content="2;url=/applications">
    <div class="container">
      <div class="card">
        <h1>🧠 Python Developer Roadmap</h1>
        <p>Select a learning level to explore detailed concepts.</p>

        <div class="nav">
          <a href="/applications" target="_blank"><button>Required Applications</button></a>
          <a href="/fresher"><button>Fresher</button></a>
          <a href="/intermediate"><button>Intermediate</button></a>
          <a href="/advanced"><button>Advanced</button></a>
          <a href="/experienced"><button>Experienced</button></a>
          <a href="/skill-gap"><button>🧠 Skill Gap Analyzer</button></a>
          <a href="/resume-analyzer"><button>📄 Resume Analyzer</button></a>

        </div>
      </div>
    </div>
    """)
# -------------------------------
# REQUIRED APPLICATIONS PAGE
# -------------------------------
@app.route("/applications")
def applications():
    return render_template_string(base_css + """
    <div class="container">
      <div class="card">
        <h2>🛠 Required Applications to Run Python Code</h2>
        <p>
          Install the following tools to write, run, and manage Python programs.
          Choose your operating system to download the correct version.
        </p>

        <hr>

        <h3>🐍 Python (Official)</h3>
        <a href="https://www.python.org/downloads/windows/" target="_blank">
          <button>Windows</button>
        </a>
        <a href="https://www.python.org/downloads/macos/" target="_blank">
          <button>macOS</button>
        </a>
        <a href="https://www.python.org/downloads/source/" target="_blank">
          <button>Linux</button>
        </a>

        <hr>

        <h3>💻 Visual Studio Code</h3>
        <a href="https://code.visualstudio.com/Download" target="_blank">
          <button>Windows</button>
        </a>
        <a href="https://code.visualstudio.com/Download" target="_blank">
          <button>macOS</button>
        </a>
        <a href="https://code.visualstudio.com/Download" target="_blank">
          <button>Linux</button>
        </a>

        <hr>

        <h3>🚀 PyCharm (Community Edition)</h3>
        <a href="https://www.jetbrains.com/pycharm/download/#section=windows" target="_blank">
          <button>Windows</button>
        </a>
        <a href="https://www.jetbrains.com/pycharm/download/#section=mac" target="_blank">
          <button>macOS</button>
        </a>
        <a href="https://www.jetbrains.com/pycharm/download/#section=linux" target="_blank">
          <button>Linux</button>
        </a>

        <hr>

        <h3>🌿 Git (Version Control)</h3>
        <a href="https://git-scm.com/download/win" target="_blank">
          <button>Windows</button>
        </a>
        <a href="https://git-scm.com/download/mac" target="_blank">
          <button>macOS</button>
        </a>
        <a href="https://git-scm.com/download/linux" target="_blank">
          <button>Linux</button>
        </a>

        <hr>

        <h3>🔗 Postman (API Testing)</h3>
        <a href="https://www.postman.com/downloads/" target="_blank">
          <button>Download</button>
        </a>

        <hr>

        <a href="/levels"><button>⬅ Back to Roadmap</button></a>
      </div>
    </div>
    """)


# -------------------------------
# FRESHER PAGE 
# -------------------------------
@app.route("/fresher")
def fresher():
    return render_template_string(base_css + """
    <div class="container">
      <div class="card">
        <h2>🌱 Fresher / Beginner Level</h2>
        <p>
          This level builds <b>strong Python foundations</b> required for entry-level
          Python developer roles. It focuses on understanding the language deeply,
          writing clean code, and applying concepts through hands-on practice.
        </p>

        <ul>
          <li>
            <b>Python Basics & Syntax</b><br>
            <small>
            Learn Python structure, indentation rules, variables, keywords,
            comments, and program execution flow.
            </small><br>
            📘 Notes: 
            <a href="https://docs.python.org/3/tutorial/index.html" target="_blank">
              Python Official Tutorial
            </a><br>
            🎥 YouTube: 
            <a href="https://www.youtube.com/watch?v=rfscVS0vtbw" target="_blank">
              Python Full Course – freeCodeCamp
            </a>
          </li>

          <li>
            <b>Data Types & Collections</b><br>
            <small>
            Understand integers, floats, strings, booleans, and Python collections
            like Lists, Tuples, Sets, and Dictionaries for managing real-world data.
            </small><br>
            📘 Notes: 
            <a href="https://docs.python.org/3/tutorial/datastructures.html" target="_blank">
              Python Data Structures
            </a><br>
            🎥 YouTube:
            <a href="https://www.youtube.com/watch?v=W8KRzm-HUcc" target="_blank">
              Python Lists & Dictionaries – Corey Schafer
            </a>
          </li>

          <li>
            <b>Control Structures & Functions</b><br>
            <small>
            Learn decision-making using if-else, looping using for and while,
            and reusable code using functions and parameters.
            </small><br>
            📘 Notes:
            <a href="https://www.programiz.com/python-programming/if-elif-else" target="_blank">
              Control Flow – Programiz
            </a><br>
            🎥 YouTube:
            <a href="https://www.youtube.com/watch?v=9Os0o3wzS_I" target="_blank">
              Python Functions – Corey Schafer
            </a>
          </li>

          <li>
            <b>String Manipulation</b><br>
            <small>
            Process and clean text data using slicing, string methods,
            formatting, and user input handling.
            </small><br>
            📘 Notes:
            <a href="https://www.programiz.com/python-programming/string" target="_blank">
              Python Strings
            </a><br>
            🎥 YouTube:
            <a href="https://www.youtube.com/watch?v=k9TUPpGqYTo" target="_blank">
              Python Strings Explained
            </a>
          </li>

          <li>
            <b>File Handling</b><br>
            <small>
            Learn to read from and write to files for data storage,
            reports, and simple databases.
            </small><br>
            📘 Notes:
            <a href="https://www.programiz.com/python-programming/file-operation" target="_blank">
              File Handling in Python
            </a><br>
            🎥 YouTube:
            <a href="https://www.youtube.com/watch?v=Uh2ebFW8OYM" target="_blank">
              File Handling – Corey Schafer
            </a>
          </li>

          <li>
            <b>Exception Handling</b><br>
            <small>
            Handle runtime errors using try, except, else, and finally
            to make applications stable and user-friendly.
            </small><br>
            📘 Notes:
            <a href="https://docs.python.org/3/tutorial/errors.html" target="_blank">
              Errors & Exceptions
            </a><br>
            🎥 YouTube:
            <a href="https://www.youtube.com/watch?v=NIWwJbo-9_8" target="_blank">
              Python Exceptions – Corey Schafer
            </a>
          </li>

          <li>
            <b>Modules & Packages</b><br>
            <small>
            Organize code using modules and packages and reuse built-in
            and external Python libraries.
            </small><br>
            📘 Notes:
            <a href="https://docs.python.org/3/tutorial/modules.html" target="_blank">
              Python Modules
            </a><br>
            🎥 YouTube:
            <a href="https://www.youtube.com/watch?v=1RuMJ53CKds" target="_blank">
              Python Modules Explained
            </a>
          </li>

          <li>
            <b>Object-Oriented Programming (OOP)</b><br>
            <small>
            Learn classes, objects, inheritance, encapsulation, and polymorphism
            to build scalable applications.
            </small><br>
            📘 Notes:
            <a href="https://www.programiz.com/python-programming/object-oriented-programming" target="_blank">
              OOP in Python
            </a><br>
            🎥 YouTube:
            <a href="https://www.youtube.com/watch?v=JeznW_7DlB0" target="_blank">
              OOP in Python – Corey Schafer
            </a>
          </li>

          <li>
            <b>Mini Projects (Hands-On)</b><br>
            <small>
            Apply all concepts by building:
            Calculator, Student Management System, File-Based App.
            </small><br>
            🧪 Practice Platforms:
            <a href="https://www.hackerrank.com/domains/tutorials/10-days-of-python" target="_blank">
              HackerRank – Python
            </a>,
            <a href="https://leetcode.com/problemset/all/?difficulty=EASY" target="_blank">
              LeetCode Easy
            </a>,
            <a href="https://github.com/" target="_blank">
              GitHub (Project Hosting)
            </a>
          </li>
        </ul>
                                  <hr>

<h3>🎯 Entry-Level Job Roles You Can Target</h3>
<ul>
  <li>Junior Python Developer</li>
  <li>Python Trainee / Intern</li>
  <li>Software Developer (Entry Level)</li>
  <li>Backend Developer – Junior</li>
</ul>

<h3>💡 Learning Tips for Freshers</h3>
<ul>
  <li>Consistency beats intensity – code daily</li>
  <li>Practice each concept with small programs</li>
  <li>Don’t memorize, understand the logic</li>
  <li>Use GitHub to save your practice and projects</li>
</ul>

<h3>🌟 Motivation to Stay Consistent</h3>
<p>
  “Every expert was once a beginner.”<br>
  “Small steps every day lead to big results.”<br>
  “Don’t rush the process. Learn deeply.”
</p>

<h3>🗓️ Recommended Fresher Study Plan</h3>
<ul>
  <li>Week 1–2: Python basics & data types</li>
  <li>Week 3: Control structures & functions</li>
  <li>Week 4: Strings & file handling</li>
  <li>Week 5: Exceptions, modules & packages</li>
  <li>Week 6: Object-Oriented Programming</li>
  <li>Week 7–8: Mini projects & revision</li>
</ul>

<a href="/fresher-study-plan-pdf">
  <button>📄 Download Study Plan as PDF</button>
</a>
<a href="/levels"><button>Back</button></a>
      </div>
    </div>
    """)
      
@app.route("/intermediate-study-plan-pdf")
def intermediate_study_plan_pdf():
    from reportlab.platypus import SimpleDocTemplate, Paragraph
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.pagesizes import A4
    from flask import send_file
    import tempfile

    styles = getSampleStyleSheet()

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    temp_file.close()

    doc = SimpleDocTemplate(temp_file.name, pagesize=A4)
    content = []

    content.append(Paragraph("Python Intermediate Study Plan", styles["Title"]))
    content.append(Paragraph(
        "Goal: Become a job-ready Python Backend Developer with real-world skills.",
        styles["Normal"]
    ))

    plan = [
        "Week 1: Flask fundamentals, app structure, routing",
        "Week 2: Templates, forms, CRUD operations",
        "Week 3: Databases (SQLite/MySQL) & SQLAlchemy ORM",
        "Week 4: REST APIs, JSON handling, HTTP methods",
        "Week 5: Authentication, sessions, protected routes",
        "Week 6: Error handling, logging, debugging",
        "Week 7: API testing using Postman",
        "Week 8: Version control with Git & GitHub",
        "Week 9–10: Intermediate Projects (CRUD app, Auth system, REST API)"
    ]

    for item in plan:
        content.append(Paragraph(item, styles["Normal"]))

    content.append(Paragraph(
        "Tip: Build projects side-by-side while learning. Don’t wait to be perfect.",
        styles["Italic"]
    ))

    doc.build(content)

    return send_file(
        temp_file.name,
        as_attachment=True,
        download_name="Python_Intermediate_Study_Plan.pdf"
    )


# -------------------------------
# INTERMEDIATE PAGE
# -------------------------------
@app.route("/intermediate")
def intermediate():
    return render_template_string(base_css + """
    <div class="container">
      <div class="card">
        <h2>🚀 Intermediate Level</h2>
        <p>
          This level focuses on <b>real-world backend development using Python</b>.
          Learners move from writing scripts to building structured, secure,
          database-driven web applications and APIs used in industry.
        </p>

        <ul>
          <li>
            <b>Flask Web Framework (In-Depth)</b><br>
            <small>
              Learn Flask application structure, routing, templates, static files,
              configuration management, and modular design using Blueprints.
            </small><br>
            📘 Notes:
            <a href="https://flask.palletsprojects.com/en/latest/" target="_blank">
              Flask Official Documentation
            </a><br>
            🎥 YouTube:
            <a href="https://www.youtube.com/watch?v=Z1RJmh_OqeA" target="_blank">
              Flask Tutorial – Corey Schafer
            </a>
          </li>

          <li>
            <b>CRUD Operations (Real-World Data Handling)</b><br>
            <small>
              Implement Create, Read, Update, and Delete operations with form handling,
              validation, error handling, pagination, and filtering.
            </small><br>
            📘 Notes:
            <a href="https://www.geeksforgeeks.org/crud-operations-in-python/" target="_blank">
              CRUD Operations in Python
            </a><br>
            🎥 YouTube:
            <a href="https://www.youtube.com/watch?v=wj2F1VtYtck" target="_blank">
              Flask CRUD Application Tutorial
            </a>
          </li>

          <li>
            <b>Database Integration & ORM (SQLAlchemy)</b><br>
            <small>
              Work with relational databases like SQLite/MySQL, design schemas,
              use SQLAlchemy ORM, and manage relationships between tables.
            </small><br>
            📘 Notes:
            <a href="https://docs.sqlalchemy.org/en/20/orm/" target="_blank">
              SQLAlchemy ORM Documentation
            </a><br>
            🎥 YouTube:
            <a href="https://www.youtube.com/watch?v=cYWiDiIUxQc" target="_blank">
              SQLAlchemy Tutorial – Corey Schafer
            </a>
          </li>

          <li>
            <b>REST API Development</b><br>
            <small>
              Build RESTful APIs using Flask, handle JSON requests and responses,
              use proper HTTP methods, and return correct status codes.
            </small><br>
            📘 Notes:
            <a href="https://restfulapi.net/" target="_blank">
              REST API Concepts
            </a><br>
            🎥 YouTube:
            <a href="https://www.youtube.com/watch?v=GMppyAPbLYk" target="_blank">
              REST API with Flask
            </a>
          </li>

          <li>
            <b>Authentication & Session Management</b><br>
            <small>
              Implement login and logout flows, manage user sessions,
              and protect routes that require authentication.
            </small><br>
            📘 Notes:
            <a href="https://flask-login.readthedocs.io/en/latest/" target="_blank">
              Flask-Login Documentation
            </a><br>
            🎥 YouTube:
            <a href="https://www.youtube.com/watch?v=8aTnmsDMldY" target="_blank">
              Flask Login System Tutorial
            </a>
          </li>

          <li>
            <b>Error Handling, Debugging & Logging</b><br>
            <small>
              Debug backend issues, handle exceptions gracefully,
              log application activity, and understand stack traces.
            </small><br>
            📘 Notes:
            <a href="https://docs.python.org/3/library/logging.html" target="_blank">
              Python Logging Module
            </a><br>
            🎥 YouTube:
            <a href="https://www.youtube.com/watch?v=-ARI4Cz-awo" target="_blank">
              Debugging & Logging in Python
            </a>
          </li>

          <li>
            <b>API Testing & Development Tools</b><br>
            <small>
              Test APIs using Postman, validate headers, payloads,
              and responses to ensure reliability.
            </small><br>
            📘 Tool:
            <a href="https://www.postman.com/" target="_blank">
              Postman Official Website
            </a><br>
            🎥 YouTube:
            <a href="https://www.youtube.com/watch?v=VywxIQ2ZXw4" target="_blank">
              Postman API Testing Tutorial
            </a>
          </li>

          <li>
            <b>Version Control (Git & GitHub)</b><br>
            <small>
              Track code changes, collaborate using GitHub,
              manage branches, and maintain project repositories.
            </small><br>
            📘 Notes:
            <a href="https://git-scm.com/doc" target="_blank">
              Git Official Documentation
            </a><br>
            🎥 YouTube:
            <a href="https://www.youtube.com/watch?v=RGOj5yH7evk" target="_blank">
              Git & GitHub Crash Course
            </a>
          </li>

          <li>
            <b>Intermediate-Level Projects</b><br>
            <small>
              • CRUD Web Application (Flask + Database)<br>
              • User Authentication System<br>
              • REST API Project (tested using Postman)
            </small><br>
            🧪 Practice Platforms:
            <a href="https://www.hackerrank.com/domains/python" target="_blank">
              HackerRank
            </a>,
            <a href="https://leetcode.com/problemset/all/?difficulty=MEDIUM" target="_blank">
              LeetCode (Medium)
            </a>,
            <a href="https://github.com/" target="_blank">
              GitHub (Project Hosting)
            </a>
          </li>
        </ul>
                                  <hr>

<h3>🎯 Job Roles You Can Target (After Intermediate)</h3>
<ul>
  <li>Python Backend Developer (Junior)</li>
  <li>Junior Software Engineer</li>
  <li>Backend Developer – Entry Level</li>
  <li>Python Web Developer</li>
</ul>

<h3>💡 Learning Tips for Intermediate Learners</h3>
<ul>
  <li>Build projects while learning each topic</li>
  <li>Understand why things work, not just how</li>
  <li>Read error messages carefully — they are your teachers</li>
  <li>Push every project to GitHub with a proper README</li>
</ul>

<h3>🌟 Motivation to Stay Consistent</h3>
<p>
  “You don’t need to know everything — you need to know enough to build.”<br>
  “Confusion means growth. Keep going.”
</p>

<h3>🗓️ Recommended Intermediate Study Plan</h3>
<ul>
  <li>Week 1–2: Flask fundamentals & CRUD</li>
  <li>Week 3: Databases & ORM</li>
  <li>Week 4: REST APIs</li>
  <li>Week 5: Authentication & sessions</li>
  <li>Week 6: Debugging & logging</li>
  <li>Week 7: API testing (Postman)</li>
  <li>Week 8–10: Projects & revision</li>
</ul>

<a href="/intermediate-study-plan-pdf">
  <button>📄 Download Intermediate Study Plan (PDF)</button>
</a>


        <a href="/levels"><button>Back</button></a>
      </div>
    </div>
    """)
@app.route("/advanced-study-plan-pdf")
def advanced_study_plan_pdf():
    from reportlab.platypus import SimpleDocTemplate, Paragraph
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.pagesizes import A4
    from flask import send_file
    import tempfile

    styles = getSampleStyleSheet()

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    temp_file.close()

    doc = SimpleDocTemplate(temp_file.name, pagesize=A4)
    content = []

    content.append(Paragraph("Python Advanced Study Plan", styles["Title"]))
    content.append(Paragraph(
        "Goal: Build production-ready, secure, and scalable Python backend systems.",
        styles["Normal"]
    ))

    plan = [
        "Week 1: Advanced authentication (JWT, RBAC)",
        "Week 2: API optimization & performance tuning",
        "Week 3: Advanced database design & query optimization",
        "Week 4: Centralized error handling & logging",
        "Week 5: Deployment fundamentals & environment management",
        "Week 6: Docker basics & CI/CD concepts",
        "Week 7: Advanced API design & architecture",
        "Week 8–9: Advanced Projects (Secure API, Optimized Backend)",
        "Week 10: Revision & system-level understanding"
    ]

    for item in plan:
        content.append(Paragraph(item, styles["Normal"]))

    content.append(Paragraph(
        "Tip: Think like a system owner. Focus on reliability, security, and performance.",
        styles["Italic"]
    ))

    doc.build(content)

    return send_file(
        temp_file.name,
        as_attachment=True,
        download_name="Python_Advanced_Study_Plan.pdf"
    )

# -------------------------------
# ADVANCED PAGE 
# -------------------------------
@app.route("/advanced")
def advanced():
    return render_template_string(base_css + """
    <div class="container">
      <div class="card">
        <h2>⚡ Advanced Level</h2>
        <p>
          The Advanced level focuses on building <b>production-ready, secure,
          optimized, and scalable backend systems</b>. Learners gain expertise
          in performance, security, deployment, and architecture required for
          mid-level Python backend roles.
        </p>

        <ul>
          <li>
            <b>Advanced Authentication & Authorization</b><br>
            <small>
              Implement secure authentication systems using password hashing,
              role-based access control (RBAC), token-based authentication (JWT),
              and protecting APIs and routes.
            </small><br>
            📘 Notes:
            <a href="https://flask-login.readthedocs.io/en/latest/" target="_blank">
              Flask-Login Documentation
            </a>,
            <a href="https://jwt.io/introduction" target="_blank">
              JWT Introduction
            </a><br>
            🎥 YouTube:
            <a href="https://www.youtube.com/watch?v=WxGBoY5iNXY" target="_blank">
              JWT Authentication in Python
            </a>
          </li>

          <li>
            <b>API Optimization & Performance Engineering</b><br>
            <small>
              Optimize APIs by improving database queries, reducing response time,
              implementing pagination, caching strategies (Redis – conceptual),
              and handling performance bottlenecks.
            </small><br>
            📘 Notes:
            <a href="https://developer.mozilla.org/en-US/docs/Web/Performance" target="_blank">
              Web Performance Concepts (MDN)
            </a><br>
            🎥 YouTube:
            <a href="https://www.youtube.com/watch?v=9U_5p-YjzG0" target="_blank">
              API Performance Optimization
            </a>
          </li>

          <li>
            <b>Advanced Database Design & Optimization</b><br>
            <small>
              Learn indexing, normalization vs denormalization,
              query optimization, handling large datasets,
              and transaction management concepts.
            </small><br>
            📘 Notes:
            <a href="https://use-the-index-luke.com/" target="_blank">
              Database Indexing Guide
            </a><br>
            🎥 YouTube:
            <a href="https://www.youtube.com/watch?v=H5nS1nO5dVY" target="_blank">
              Database Optimization Explained
            </a>
          </li>

          <li>
            <b>Production-Level Error Handling & Logging</b><br>
            <small>
              Implement centralized error handling, structured logging,
              monitoring application health, and debugging production issues.
            </small><br>
            📘 Notes:
            <a href="https://docs.python.org/3/library/logging.html" target="_blank">
              Python Logging Documentation
            </a><br>
            🎥 YouTube:
            <a href="https://www.youtube.com/watch?v=-ARI4Cz-awo" target="_blank">
              Logging Best Practices in Python
            </a>
          </li>

          <li>
            <b>Deployment & DevOps Fundamentals</b><br>
            <small>
              Deploy applications using platforms like Render/AWS/GCP (conceptual),
              manage environment variables, understand Docker basics,
              and CI/CD pipeline fundamentals.
            </small><br>
            📘 Notes:
            <a href="https://docs.docker.com/get-started/" target="_blank">
              Docker Getting Started
            </a><br>
            🎥 YouTube:
            <a href="https://www.youtube.com/watch?v=3c-iBn73dDE" target="_blank">
              Docker Explained Simply
            </a>
          </li>

          <li>
            <b>Advanced API Design & Architecture</b><br>
            <small>
              Design scalable APIs using best REST practices,
              API versioning, proper endpoint structure,
              and understanding monolithic vs microservices architecture.
            </small><br>
            📘 Notes:
            <a href="https://restfulapi.net/best-practices/" target="_blank">
              REST API Best Practices
            </a><br>
            🎥 YouTube:
            <a href="https://www.youtube.com/watch?v=Q-BpqyOT3a8" target="_blank">
              API Design Principles
            </a>
          </li>

          <li>
            <b>Advanced-Level Projects</b><br>
            <small>
              • Secure Authentication System with JWT<br>
              • Optimized REST API with pagination & caching<br>
              • Fully Deployed Production Backend Application
            </small><br>
            🧪 Practice & Project Platforms:
            <a href="https://www.hackerrank.com/domains/python" target="_blank">
              HackerRank
            </a>,
            <a href="https://leetcode.com/problemset/all/?difficulty=HARD" target="_blank">
              LeetCode (Medium–Hard)
            </a>,
            <a href="https://github.com/" target="_blank">
              GitHub
            </a>
          </li>
        </ul>
                                  <hr>

<h3>🎯 Job Roles You Can Target (After Advanced)</h3>
<ul>
  <li>Python Backend Developer</li>
  <li>Backend Engineer</li>
  <li>Python API Developer</li>
  <li>Software Engineer (Backend)</li>
</ul>

<h3>💡 Learning Tips for Advanced Learners</h3>
<ul>
  <li>Focus on “why” a design choice is made, not just “how”</li>
  <li>Read production-grade code on GitHub</li>
  <li>Optimize before scaling, not after</li>
  <li>Practice explaining your design decisions</li>
</ul>

<h3>🌟 Motivation to Stay Consistent</h3>
<p>
  “Advanced developers are not faster — they are more thoughtful.”<br>
  “Every refactor makes you a better engineer.”
</p>

<h3>🗓️ Recommended Advanced Study Plan</h3>
<ul>
  <li>Week 1–2: Security & authentication</li>
  <li>Week 3: API & database optimization</li>
  <li>Week 4: Logging, monitoring & debugging</li>
  <li>Week 5–6: Deployment & DevOps basics</li>
  <li>Week 7–9: Advanced projects</li>
  <li>Week 10: Review & architectural thinking</li>
</ul>

<a href="/advanced-study-plan-pdf">
  <button>📄 Download Advanced Study Plan (PDF)</button>
</a>


        <a href="/levels"><button>Back</button></a>
      </div>
    </div>
    """)
@app.route("/experienced-study-plan-pdf")
def experienced_study_plan_pdf():
    from reportlab.platypus import SimpleDocTemplate, Paragraph
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.pagesizes import A4
    from flask import send_file
    import tempfile

    styles = getSampleStyleSheet()

    # Create a temporary PDF file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    temp_file.close()

    doc = SimpleDocTemplate(temp_file.name, pagesize=A4)
    content = []

    content.append(Paragraph("Python Experienced (Senior) Study Plan", styles["Title"]))
    content.append(Paragraph(
        "Goal: Develop senior-level system design, scalability, security, and leadership skills "
        "required to own and architect large-scale backend systems.",
        styles["Normal"]
    ))

    plan = [
        "Week 1: System design fundamentals & architecture patterns",
        "Week 2: Scalability strategies, caching, and async processing",
        "Week 3: Advanced security, OWASP Top 10, and reliability engineering",
        "Week 4: Observability, monitoring, logging, and incident response",
        "Week 5: Cloud architecture (AWS/GCP concepts) & DevOps practices",
        "Week 6: CI/CD pipelines, containerization & infrastructure concepts",
        "Week 7–8: Senior-level projects (scalable backend, enterprise app)",
        "Week 9: System design case studies (URL shortener, e-commerce, chat)",
        "Week 10: Mentoring mindset, code reviews, and architectural reviews"
    ]

    for item in plan:
        content.append(Paragraph(item, styles["Normal"]))

    content.append(Paragraph(
        "Tip: Senior engineers think in terms of systems, trade-offs, and long-term impact.",
        styles["Italic"]
    ))

    doc.build(content)

    return send_file(
        temp_file.name,
        as_attachment=True,
        download_name="Python_Experienced_Study_Plan.pdf"
    )

# -------------------------------
# EXPERIENCED PAGE 
# -------------------------------
@app.route("/experienced")
def experienced():
    return render_template_string(base_css + """
    <div class="container">
      <div class="card">
        <h2>🏆 Experienced Level</h2>
        <p>
          The Experienced level focuses on <b>senior and lead-level backend engineering</b>.
          Learners master system design, scalability, security, cloud architecture,
          observability, and leadership skills required to own large-scale systems
          and mentor teams.
        </p>

        <ul>
          <li>
            <b>System Design & Architecture</b><br>
            <small>
              Design large-scale systems using layered architecture, clean architecture,
              and microservices concepts. Understand load balancing, fault tolerance,
              and high availability.
            </small><br>
            📘 Notes:
            <a href="https://github.com/donnemartin/system-design-primer" target="_blank">
              System Design Primer (GitHub)
            </a><br>
            🎥 YouTube:
            <a href="https://www.youtube.com/watch?v=UzLMhqg3_Wc" target="_blank">
              System Design Basics
            </a>
          </li>

          <li>
            <b>Scalability & Performance at Scale</b><br>
            <small>
              Handle high traffic using horizontal & vertical scaling,
              caching strategies (Redis – conceptual),
              asynchronous processing, and concurrency control.
            </small><br>
            📘 Notes:
            <a href="https://aws.amazon.com/builders-library/" target="_blank">
              AWS Builders Library
            </a><br>
            🎥 YouTube:
            <a href="https://www.youtube.com/watch?v=9s8XjzA4q8k" target="_blank">
              Scalability Explained
            </a>
          </li>

          <li>
            <b>Advanced Security & Reliability Engineering</b><br>
            <small>
              Apply OWASP Top 10, secure API design, rate limiting,
              secrets management, data privacy, and disaster recovery planning.
            </small><br>
            📘 Notes:
            <a href="https://owasp.org/www-project-top-ten/" target="_blank">
              OWASP Top 10
            </a><br>
            🎥 YouTube:
            <a href="https://www.youtube.com/watch?v=EyrGm0E4J6o" target="_blank">
              Web Security Explained
            </a>
          </li>

          <li>
            <b>Observability, Monitoring & Incident Management</b><br>
            <small>
              Implement logging, metrics, tracing, alerts, health checks,
              and perform root-cause analysis for production issues.
            </small><br>
            📘 Notes:
            <a href="https://sre.google/sre-book/table-of-contents/" target="_blank">
              Google SRE Book
            </a><br>
            🎥 YouTube:
            <a href="https://www.youtube.com/watch?v=K5y8KJ4cZ98" target="_blank">
              Monitoring & Observability
            </a>
          </li>

          <li>
            <b>Cloud Architecture & Advanced DevOps</b><br>
            <small>
              Design cloud-native systems using AWS/GCP concepts,
              containerization with Docker, Kubernetes basics,
              CI/CD pipelines, and infrastructure as code.
            </small><br>
            📘 Notes:
            <a href="https://cloud.google.com/architecture" target="_blank">
              Google Cloud Architecture Center
            </a><br>
            🎥 YouTube:
            <a href="https://www.youtube.com/watch?v=3c-iBn73dDE" target="_blank">
              Kubernetes Explained Simply
            </a>
          </li>

          <li>
            <b>Engineering Leadership & Best Practices</b><br>
            <small>
              Conduct code reviews, mentor developers, write technical documentation,
              manage technical debt, and apply Agile & SDLC principles.
            </small><br>
            📘 Notes:
            <a href="https://martinfowler.com/" target="_blank">
              Martin Fowler Articles
            </a><br>
            🎥 YouTube:
            <a href="https://www.youtube.com/watch?v=ZK8EJ2P9N0A" target="_blank">
              How Senior Engineers Think
            </a>
          </li>

          <li>
            <b>Experienced-Level Projects</b><br>
            <small>
              • Design a scalable backend system (microservices-style)<br>
              • Enterprise-grade cloud-deployed application<br>
              • System design case studies (URL shortener, e-commerce, chat system)
            </small><br>
            🧪 Practice & Project Platforms:
            <a href="https://github.com/" target="_blank">
              GitHub
            </a>,
            <a href="https://leetcode.com/problemset/all/?difficulty=HARD" target="_blank">
              LeetCode (Hard)
            </a>,
            <a href="https://exercism.org/tracks/python" target="_blank">
              Exercism – Python
            </a>
          </li>
        </ul>
                                  <hr>

<h3>🎯 Senior-Level Job Roles You Can Target</h3>
<ul>
  <li>Senior Python Developer</li>
  <li>Senior Backend Engineer</li>
  <li>Technical Lead / Backend Lead</li>
  <li>System Architect (Junior–Mid)</li>
  <li>Platform Engineer</li>
</ul>

<h3>💡 Tips for Experienced / Senior Learners</h3>
<ul>
  <li>Think in terms of systems, not just features</li>
  <li>Always consider scalability, security, and maintainability</li>
  <li>Practice explaining architectural decisions clearly</li>
  <li>Mentor juniors — teaching strengthens mastery</li>
</ul>

<h3>🌟 Motivation to Stay Consistent at Senior Level</h3>
<p>
  “Senior engineers are defined by judgment, not just knowledge.”<br>
  “Leadership begins with responsibility, not title.”
</p>

<h3>🗓️ Recommended Experienced Study Plan</h3>
<ul>
  <li>Week 1–2: System design & architecture patterns</li>
  <li>Week 3: Scalability, caching & async processing</li>
  <li>Week 4: Security, reliability & failure handling</li>
  <li>Week 5: Observability & production monitoring</li>
  <li>Week 6: Cloud architecture & DevOps concepts</li>
  <li>Week 7–8: Senior-level projects</li>
  <li>Week 9–10: Case studies & leadership practices</li>
</ul>

<a href="/experienced-study-plan-pdf">
  <button>📄 Download Experienced Study Plan (PDF)</button>
</a>


        <a href="/levels"><button>Back</button></a>
      </div>
    </div>
    """)
# ================================
# ADD-ONS: SKILL GAP + RESUME ANALYZER
# ================================

# -------------------------------
# SKILL GAP DATA
# -------------------------------
EXPECTED_SKILLS = {
    "fresher": [
        "python basics", "data types", "loops", "functions",
        "strings", "file handling", "oop"
    ],
    "intermediate": [
        "flask", "crud", "sql", "sqlalchemy",
        "rest api", "authentication", "git"
    ],
    "advanced": [
        "jwt", "api optimization", "logging",
        "docker", "deployment", "system design"
    ]
}

# -------------------------------
# SKILL GAP ANALYSIS PAGE
# -------------------------------
@app.route("/skill-gap", methods=["GET", "POST"])
def skill_gap():
    result_html = ""

    if request.method == "POST":
        level = request.form["level"]
        user_skills = request.form["skills"].lower().split(",")

        expected = EXPECTED_SKILLS[level]
        user_skills = [s.strip() for s in user_skills]

        matched = [s for s in expected if s in user_skills]
        missing = [s for s in expected if s not in user_skills]
        total = len(expected)
        score = int((len(matched) / total) * 100)


        result_html = f"""
        <h3>📊 Skill Gap Analysis Result</h3>
        <p><b>Level Selected:</b> {level.capitalize()}</p>

        <h4>✅ Skills You Have</h4>
        <ul>{"".join(f"<li>{s}</li>" for s in matched)}</ul>

        <h4>❌ Missing Skills</h4>
        <ul>{"".join(f"<li>{s}</li>" for s in missing)}</ul>

        <p><b>Suggestion:</b> Focus on the missing skills to become job-ready.</p>
        """
        result_html += f"""
<hr>

<h3>📊 Skill Readiness Meter</h3>

<div class="gauge-container">
  <div class="gauge">
    <div class="gauge-fill" style="transform: rotate({score * 1.8}deg);"></div>
    <div class="gauge-cover">
      <span>{score}%</span>
    </div>
  </div>
  <p><b>Job Readiness Level</b></p>
</div>
"""


    return render_template_string(base_css + f"""
    <div class="container">
      <div class="card">
        <h2>🧠 Python Skill Gap Analyzer</h2>
        <p>Check where you stand and what you need to improve.</p>

        <form method="POST">
          <label>Select Your Level</label><br><br>
          <select name="level" required style="width:100%;padding:12px;border-radius:10px;">
            <option value="" disabled selected>Select Level</option>                     
            <option value="fresher">Fresher</option>
            <option value="intermediate">Intermediate</option>
            <option value="advanced">Advanced</option>
          </select><br><br>

          <label>Enter Your Current Skills (comma separated)</label><br><br>
          <input name="skills" placeholder="python basics, loops, functions...."
            style="width:100%;padding:12px;border-radius:10px;" required>

          <button style="margin-top:20px;width:100%;">Analyze</button>
        </form>

        <hr>
        {result_html}

        <a href="/levels"><button>Back</button></a>
      </div>
    </div>
    """)

# -------------------------------
# RESUME ANALYZER PAGE
# -------------------------------
@app.route("/resume-analyzer", methods=["GET", "POST"])
def resume_analyzer():
    analysis_html = ""

    REQUIRED_RESUME_SKILLS = [
        "python", "flask", "sql", "api",
        "git", "oop", "database", "projects"
    ]
    if request.method == "POST":
        file = request.files.get("resume")

        if file and file.filename:
            filename = secure_filename(file.filename)
            text = ""

            # TXT resume
            if filename.endswith(".txt"):
                text = file.read().decode("utf-8", errors="ignore").lower()

            # PDF resume
            elif filename.endswith(".pdf"):
                reader = PdfReader(file)
                for page in reader.pages:
                    text += page.extract_text().lower()


        found = [s for s in REQUIRED_RESUME_SKILLS if s in text]
        missing = [s for s in REQUIRED_RESUME_SKILLS if s not in text]

        analysis_html = f"""
        <h3>📄 Resume Analysis Result</h3>

        <h4>✅ Skills Found in Resume</h4>
        <ul>{"".join(f"<li>{s}</li>" for s in found)}</ul>

        <h4>❌ Missing / Weak Areas</h4>
        <ul>{"".join(f"<li>{s}</li>" for s in missing)}</ul>

        <p><b>Tip:</b> Add missing skills with projects or hands-on experience.</p>
        """

    return render_template_string(base_css + f"""
    <div class="container">
      <div class="card">
        <h2>📄 Python Resume Analyzer</h2>
        <p>Paste your resume content to detect missing Python skills.</p>

        <form method="POST" enctype="multipart/form-data">
        <input type="file" name="resume" accept=".txt,.pdf"
  style="width:100%;padding:14px;border-radius:10px;" required>


          <button style="margin-top:20px;width:100%;">Analyze Resume</button>
        </form>

        <hr>
        {analysis_html}
        <hr>

<h3>📄 Download Python Resume Templates</h3>
<p>Use these ATS-friendly templates and customize them.</p>

<a href="/download-resume/fresher"><button>⬇ Fresher Resume</button></a>
<a href="/download-resume/intermediate"><button>⬇ Intermediate Resume</button></a>
<a href="/download-resume/advanced"><button>⬇ Advanced Resume</button></a>


        <a href="/levels"><button>Back</button></a>
      </div>
    </div>
    """)
# -------------------------------
# RESUME TEMPLATES (ADD-ON)
# -------------------------------

RESUME_TEMPLATES = {
    "fresher": """
PYTHON DEVELOPER (FRESHER)

Name:
Email | Phone | GitHub | LinkedIn

OBJECTIVE
Motivated Python fresher with strong fundamentals in Python programming,
seeking an entry-level role to apply problem-solving and backend skills.

SKILLS
• Python (Basics, Data Types, Loops, Functions)
• OOP Concepts
• File Handling
• Basic SQL
• Git & GitHub

PROJECTS
• Student Management System using Python
• File-based Application
• Calculator Application

EDUCATION
B.Tech / B.Sc / BCA – Computer Science / IT

DECLARATION
I hereby declare the information is true.
""",

    "intermediate": """
PYTHON BACKEND DEVELOPER (INTERMEDIATE)

Name:
Email | Phone | GitHub | LinkedIn

SUMMARY
Backend-focused Python developer with experience in Flask,
databases, REST APIs, and authentication.

SKILLS
• Python, Flask
• SQL, SQLAlchemy
• REST APIs
• Authentication & Sessions
• Git, GitHub
• Postman

PROJECTS
• CRUD Web Application (Flask + Database)
• Authentication System
• REST API Project

EDUCATION
Bachelor’s Degree in Computer Science / IT
""",

    "advanced": """
SENIOR PYTHON BACKEND ENGINEER

Name:
Email | Phone | GitHub | LinkedIn

PROFILE
Experienced backend engineer specializing in scalable,
secure, and production-ready Python systems.

SKILLS
• Python, Flask
• JWT, RBAC
• API Optimization
• Database Optimization
• Docker, Deployment
• System Design

PROJECTS
• Secure JWT-based Backend System
• Optimized REST API
• Cloud-deployed Backend Application

EXPERIENCE
Backend Engineer – X Years
"""
}
# -------------------------------
# RESUME TEMPLATE DOWNLOAD
# -------------------------------
@app.route("/download-resume/<level>")
def download_resume(level):
    import tempfile
    from flask import send_file

    content = RESUME_TEMPLATES.get(level)
    if not content:
        return "Template not found", 404

    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
    temp.write(content.encode("utf-8"))
    temp.close()

    return send_file(
        temp.name,
        as_attachment=True,
        download_name=f"Python_{level.capitalize()}_Resume_Template.txt"
    )




# -------------------------------
# RUN APP
# -------------------------------
from waitress import serve
import sys
import os

if __name__ == "__main__":
    # Save original stdout
    original_stdout = sys.stdout
    original_stderr = sys.stderr

    # Print ONLY the link
    print("http://127.0.0.1:5000")

    # Now silence everything else
    sys.stdout = open(os.devnull, "w")
    sys.stderr = open(os.devnull, "w")

    serve(app, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
