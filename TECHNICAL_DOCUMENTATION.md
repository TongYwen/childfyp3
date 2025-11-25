# Technical Documentation

## Preschool Performance Tracker and Learning Style Analyzer

This document provides technical details for developers working on or extending the application.

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Application Structure](#application-structure)
3. [Database Design](#database-design)
4. [Authentication System](#authentication-system)
5. [AI Integration](#ai-integration)
6. [Caching Strategy](#caching-strategy)
7. [Security Implementation](#security-implementation)
8. [API Reference](#api-reference)
9. [Development Guide](#development-guide)
10. [Deployment Guide](#deployment-guide)
11. [Testing](#testing)
12. [Performance Optimization](#performance-optimization)

---

## Architecture Overview

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Client Layer                          │
│  (Browser - HTML/CSS/JavaScript/Bootstrap)                   │
└─────────────────────┬───────────────────────────────────────┘
                      │ HTTP/HTTPS
┌─────────────────────▼───────────────────────────────────────┐
│                   Application Layer                          │
│              Flask Web Framework (Python)                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Routes     │  │  Business    │  │   Template   │      │
│  │   Handler    │  │   Logic      │  │   Rendering  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────┬───────────────────────────────────────┘
                      │
      ┌───────────────┼───────────────┐
      │               │               │
┌─────▼──────┐  ┌────▼────┐  ┌──────▼────────┐
│  Database  │  │  Email  │  │  Google AI    │
│   (MySQL)  │  │  SMTP   │  │  Gemini API   │
└────────────┘  └─────────┘  └───────────────┘
```

### Technology Stack Details

**Backend**:
- **Flask 3.x**: Lightweight WSGI web application framework
- **Flask-Login**: User session management
- **Flask-Bcrypt**: Password hashing
- **Flask-Mail**: Email functionality
- **mysql-connector-python**: MySQL database driver
- **python-dotenv**: Environment variable management
- **itsdangerous**: Cryptographic signing
- **pandas**: Data processing for benchmarks
- **google-generativeai**: Gemini AI integration

**Frontend**:
- **Jinja2**: Server-side templating
- **Bootstrap 5.3**: CSS framework
- **JavaScript (ES6)**: Client-side interactivity
- **Fetch API**: AJAX requests

**Database**:
- **MySQL 5.7+**: Relational database
- **InnoDB Engine**: Transaction support and foreign keys

---

## Application Structure

### File Organization

```
childfyp3/
├── app.py                      # Main application entry point
├── config.py                   # Configuration classes
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (not in repo)
├── .env.txt                    # Template for environment variables
├── extract_data_from_pdf.py    # Utility for PDF processing
├── test.py                     # Test scripts
│
├── static/                     # Static assets
│   ├── data/
│   │   └── developmental_milestones.csv  # Benchmark data
│   ├── style.css               # Custom CSS
│   ├── logo.png                # Application logo
│   ├── logo_words.png          # Logo with text
│   ├── background-1.jpg        # Dashboard background
│   ├── register-background.jpg # Registration background
│   ├── select-child-bg.jpg     # Child selection background
│   └── select-child.png        # Child icon
│
└── templates/                  # Jinja2 templates
    ├── base.html               # Base layout with navbar
    ├── login.html              # Login page
    ├── register_select.html    # Account type selection
    ├── register_parent.html    # Parent registration form
    ├── register_admin.html     # Admin registration form
    ├── forgot.html             # Password reset request
    ├── reset.html              # Password reset form
    ├── profile.html            # User profile page
    ├── select_child.html       # Child selection page
    ├── dashboard.html          # Main dashboard layout
    └── dashboard/              # Dashboard modules
        ├── _dashboard.html     # Dashboard home
        ├── _preschool.html     # Preschool tracker
        ├── _academic.html      # Academic progress
        ├── _learning.html      # Learning style
        ├── _tutoring.html      # Tutoring recommendations
        ├── _insights.html      # AI insights
        ├── _plan.html          # Learning plan
        └── _resources.html     # Resources hub
```

### Core Modules

#### app.py

The main application file contains:
- Flask app initialization
- Route definitions
- Business logic functions
- Database connection management
- AI integration code

**Key Components**:

```python
# Application Initialization
app = Flask(__name__)
app.config.from_object(Config)

# Extension Initialization
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
mail = Mail(app)
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

# Google Gemini Configuration
genai.configure(api_key=app.config['GOOGLE_API_KEY'])

# Benchmark Data Loading
benchmark_df = pd.read_csv("static/data/developmental_milestones.csv")
```

#### config.py

Configuration management:

```python
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    DB_HOST = os.getenv('DB_HOST')
    DB_USER = os.getenv('DB_USER')
    DB_PASS = os.getenv('DB_PASS')
    DB_NAME = os.getenv('DB_NAME')

    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True') == 'True'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')

    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
```

---

## Database Design

### Entity Relationship Diagram

```
┌──────────────┐         ┌──────────────┐
│    Users     │◄────────│  Children    │
│              │  1:N    │              │
│ id (PK)      │         │ id (PK)      │
│ name         │         │ parent_id(FK)│
│ email        │         │ name         │
│ password     │         │ dob          │
│ role         │         │ age          │
└──────────────┘         │ grade_level  │
       │                 │ gender       │
       │                 │ notes        │
       │                 └──────┬───────┘
       │                        │
       │                        │ 1:N
       │         ┌──────────────┴─────────────┬───────────────┐
       │         │                            │               │
       ▼         ▼                            ▼               ▼
┌─────────┐  ┌────────────────┐  ┌──────────────────┐  ┌─────────────┐
│  Tests  │  │   Preschool    │  │    Academic      │  │   Learning  │
│         │  │  Assessments   │  │     Scores       │  │Observations │
│ id (PK) │  │                │  │                  │  │             │
│user_id  │  │ id (PK)        │  │ id (PK)          │  │ id (PK)     │
│name     │  │ child_id (FK)  │  │ child_id (FK)    │  │child_id(FK) │
└────┬────┘  │ domain         │  │ subject          │  │observation  │
     │       │ description    │  │ score            │  └─────────────┘
     │ 1:N   │ date           │  │ date             │
     │       └────────────────┘  └──────────────────┘
     ▼
┌─────────────┐
│    Test     │
│  Questions  │
│             │
│ id (PK)     │
│ test_id(FK) │
│ question    │
│answer_type  │
└──────┬──────┘
       │ 1:N
       ▼
┌─────────────┐
│    Test     │
│   Answers   │
│             │
│ id (PK)     │
│ child_id(FK)│
│ test_id(FK) │
│question_id  │
│ answer      │
└─────────────┘

         ┌──────────────┐
         │ AI Results   │
         │              │
         │ id (PK)      │
         │ child_id(FK) │
         │ module       │
         │ data         │
         │ result       │
         │ created_at   │
         │ updated_at   │
         └──────────────┘
```

### Table Schemas

#### users
```sql
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('parent', 'admin') NOT NULL DEFAULT 'parent',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_role (role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

#### children
```sql
CREATE TABLE children (
    id INT PRIMARY KEY AUTO_INCREMENT,
    parent_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    dob DATE NOT NULL,
    age INT,
    grade_level VARCHAR(50),
    gender ENUM('Male', 'Female', 'Other'),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_parent (parent_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

#### preschool_assessments
```sql
CREATE TABLE preschool_assessments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    child_id INT NOT NULL,
    domain VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (child_id) REFERENCES children(id) ON DELETE CASCADE,
    INDEX idx_child_date (child_id, date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

#### academic_scores
```sql
CREATE TABLE academic_scores (
    id INT PRIMARY KEY AUTO_INCREMENT,
    child_id INT NOT NULL,
    subject VARCHAR(100) NOT NULL,
    score INT NOT NULL CHECK (score >= 0 AND score <= 100),
    date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (child_id) REFERENCES children(id) ON DELETE CASCADE,
    INDEX idx_child_subject (child_id, subject),
    INDEX idx_child_date (child_id, date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

#### tests
```sql
CREATE TABLE tests (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    name VARCHAR(200) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

#### test_questions
```sql
CREATE TABLE test_questions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    test_id INT NOT NULL,
    question TEXT NOT NULL,
    answer_type ENUM('text', 'scale') NOT NULL DEFAULT 'text',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (test_id) REFERENCES tests(id) ON DELETE CASCADE,
    INDEX idx_test (test_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

#### test_answers
```sql
CREATE TABLE test_answers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    child_id INT NOT NULL,
    test_id INT NOT NULL,
    question_id INT NOT NULL,
    answer TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (child_id) REFERENCES children(id) ON DELETE CASCADE,
    FOREIGN KEY (test_id) REFERENCES tests(id) ON DELETE CASCADE,
    FOREIGN KEY (question_id) REFERENCES test_questions(id) ON DELETE CASCADE,
    INDEX idx_child (child_id),
    INDEX idx_test (test_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

#### learning_observations
```sql
CREATE TABLE learning_observations (
    id INT PRIMARY KEY AUTO_INCREMENT,
    child_id INT NOT NULL,
    observation TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (child_id) REFERENCES children(id) ON DELETE CASCADE,
    INDEX idx_child (child_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

#### ai_results
```sql
CREATE TABLE ai_results (
    id INT PRIMARY KEY AUTO_INCREMENT,
    child_id INT NOT NULL,
    module VARCHAR(50) NOT NULL,
    data LONGTEXT,
    result LONGTEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (child_id) REFERENCES children(id) ON DELETE CASCADE,
    UNIQUE KEY unique_child_module (child_id, module),
    INDEX idx_child (child_id),
    INDEX idx_module (module)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### Database Connection Management

```python
def get_db_conn():
    """
    Create and return a MySQL database connection.

    Returns:
        mysql.connector.connection: Database connection object
    """
    return mysql.connector.connect(
        host=app.config['DB_HOST'],
        user=app.config['DB_USER'],
        password=app.config['DB_PASS'],
        database=app.config['DB_NAME'],
        charset='utf8mb4',
        use_unicode=True
    )
```

**Best Practices**:
- Always close connections after use
- Use `dictionary=True` cursor for named column access
- Implement connection pooling for production
- Handle connection errors gracefully

---

## Authentication System

### User Model

```python
class User(UserMixin):
    """Flask-Login user model."""

    def __init__(self, id, name, email, role):
        self.id = id
        self.name = name
        self.email = email
        self.role = role

    def get_id(self):
        """Return user ID as string for Flask-Login."""
        return str(self.id)
```

### Password Security

#### Hashing Algorithm
- **Bcrypt**: Industry-standard password hashing
- **Cost Factor**: 12 (2^12 iterations)
- **Salt**: Automatically generated per password

```python
# Password hashing
hashed = bcrypt.generate_password_hash(password).decode('utf-8')

# Password verification
is_valid = bcrypt.check_password_hash(stored_hash, provided_password)
```

#### Password Strength Requirements

```python
def is_strong_password(password: str) -> bool:
    """
    Validate password strength.

    Requirements:
    - Minimum 8 characters
    - At least one lowercase letter
    - At least one uppercase letter
    - At least one special character

    Args:
        password: Password string to validate

    Returns:
        bool: True if password meets requirements
    """
    if not password:
        return False

    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[^A-Za-z0-9])(?=.{8,})'
    return re.search(pattern, password) is not None
```

### Session Management

```python
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    """Load user from database for session."""
    conn = get_db_conn()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, name, email, role FROM users WHERE id = %s", (user_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()

    if row:
        return User(row['id'], row['name'], row['email'], row['role'])
    return None
```

### Role-Based Access Control

```python
def normalize_role(role):
    """Normalize role string for consistent checks."""
    if not role:
        return None

    normalized = str(role).strip().lower()
    aliases = {
        "administrator": "admin",
        "admin": "admin",
        "parent": "parent",
    }
    return aliases.get(normalized)

def roles_required(*roles):
    """
    Decorator to restrict access by role.

    Usage:
        @app.route('/admin/panel')
        @roles_required('admin')
        def admin_panel():
            ...
    """
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            normalized_user_role = normalize_role(current_user.role) if current_user.is_authenticated else None
            normalized_roles = [normalize_role(r) for r in roles]

            if not current_user.is_authenticated or normalized_user_role not in normalized_roles:
                flash("You don't have access to that page.", "danger")
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        return wrapped
    return wrapper
```

### Password Reset Flow

1. **Request Reset**:
```python
@app.route('/forgot', methods=['GET','POST'])
def forgot():
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        # Verify email exists
        # Generate token
        token = serializer.dumps(email, salt='password-reset-salt')
        # Send email
        send_reset_email(email, token)
```

2. **Token Validation**:
```python
@app.route('/reset/<token>', methods=['GET','POST'])
def reset_password(token):
    try:
        email = serializer.loads(token, salt='password-reset-salt', max_age=3600)  # 1 hour
    except Exception:
        flash("The reset link is invalid or expired.", "danger")
        return redirect(url_for('forgot'))
```

---

## AI Integration

### Google Gemini Setup

```python
import google.generativeai as genai

# Configure API
genai.configure(api_key=app.config['GOOGLE_API_KEY'])

# Initialize model
model = genai.GenerativeModel("gemini-2.5-flash")
```

### AI Modules

#### 1. Preschool Development Analysis

**Location**: `app.py:713-877` (`preschool_tracker()`)

**Process**:
1. Fetch child's developmental milestones
2. Calculate age in months for each milestone
3. Load benchmark dataset
4. Generate prompt with context
5. Call Gemini API
6. Cache result in `ai_results` table

**Prompt Template**:
```python
prompt = f"""
You are an early childhood development expert.

This is the data of the child: {child_info}

The following are recorded preschool milestones for a child, including their age in months when achieved:
{combined_text}

Based on these milestones, compare the child's development to standard age-based benchmarks in {benchmark_df.shape[0]} developmental records (see attached data sample below).

{benchmark_df.to_string(index=False)}

Summarize in clear, short language:
- Areas that are age-appropriate
- Areas that are delayed
- Areas that are advanced for the child's age

Follow the below rules strictly:
- End with a one-sentence summary of overall development progress.
- Provide the summary in HTML styled.
- Do not self introduce yourself.
"""
```

#### 2. Learning Style Detection

**Location**: `app.py:1001-1211` (`learning_style()`)

**Input Data**:
- Learning observations
- Test answers (text and scaled responses)

**Analysis Process**:
```python
# Combine observations
obs_text = "\n".join([f"- {o['observation']}" for o in learning_notes])

# Group test answers by test
test_grouped = {}
for ans in test_answers:
    test_grouped.setdefault(ans["test_name"], []).append(ans)

# Generate structured prompt
prompt = f"""
You are an educational psychologist specializing in early childhood learning styles.

Below are real observations and test responses for a preschool child.

Observations:
{obs_text}

Test Answers:
{ans_text}

Based on this data, identify the child's most likely learning style (Visual, Auditory, Reading/Writing, Kinesthetic, or Mixed).
Then write a short paragraph (3–5 sentences) explaining your reasoning.
Finally, list 3–5 actionable suggestions for parent to support this learning style effectively.
Keep the tone positive and easy to understand.
"""
```

#### 3. Tutoring Recommendations

**Location**: `app.py:1310-1419` (`tutoring_recommendations()`)

**Dependencies**:
- Learning style analysis result
- Preschool development analysis result

**Integration**:
```python
# Fetch previous AI results
cursor.execute("""
    SELECT module, result, updated_at FROM ai_results
    WHERE child_id=%s AND module IN ('learning', 'preschool')
""", (child_id,))

learning_result = ...
preschool_result = ...

# Generate comprehensive recommendations
prompt = f"""
You are an expert child education advisor.

--- Preschool Development Summary ---
{preschool_result if preschool_result else "No preschool data available."}

--- Learning Style Analysis ---
{learning_result if learning_result else "No learning style data available."}

Based on the above, identify:
1. The child's potential weak areas or skills that may need support.
2. Subjects or developmental domains where tutoring or extra help would be most beneficial.
3. Personalized activity or tutoring style recommendations aligned with the learning style.
"""
```

#### 4. Personalized Learning Plan

**Location**: `app.py:1571-1770` (`learning_plan()`)

**Features**:
- Weekly schedule (Monday-Sunday)
- 2-4 activities per day
- 10-20 minute duration per activity
- Aligned with learning style
- Age-appropriate activities

**Output Format**:
```html
<h3>Learning Plan Summary</h3>
<p>Parent-friendly summary...</p>

<h3>Weekly Action Plan</h3>
<table class="table table-striped">
  <thead>
    <tr><th>Day</th><th>Recommended Activities</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Monday</td>
      <td>
        <ul>
          <li>Activity 1 (10 minutes)</li>
          <li>Activity 2 (15 minutes)</li>
        </ul>
      </td>
    </tr>
    <!-- More days... -->
  </tbody>
</table>

<h3>Long-Term Strategy</h3>
<ul>
  <li>Habit 1</li>
  <li>Habit 2</li>
  ...
</ul>
```

### Error Handling

```python
try:
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)
    benchmark_summary = response.text.strip()
except Exception as e:
    error_msg = str(e)
    if "429" in error_msg or "quota" in error_msg or "token" in error_msg:
        return jsonify({"error": "token_limit"}), 429
    return jsonify({"error": f"Gemini error: {error_msg}"}), 500
```

---

## Caching Strategy

### Purpose
- Reduce API costs
- Improve response times
- Minimize redundant processing

### Implementation

**Cache Key**: `(child_id, module)` - Unique per child and AI module

**Cache Validity**:
- Determined by comparing input data JSON
- Invalid when source data changes
- Manual regeneration available

```python
# Serialize current data
data_payload = json.dumps(combined_data, default=str, ensure_ascii=False, indent=2)

# Check cached result
cursor.execute("""
    SELECT * FROM ai_results
    WHERE child_id=%s AND module='learning'
    ORDER BY created_at DESC LIMIT 1
""", (child_id,))
cached = cursor.fetchone()

# Compare data payloads
use_cached = cached and cached["data"] == data_payload and not force_regenerate

if use_cached:
    result = cached["result"]
else:
    # Call AI and cache new result
    result = call_gemini_api(prompt)

    if cached:
        # Update existing
        cursor.execute("""
            UPDATE ai_results
            SET data=%s, result=%s, updated_at=NOW()
            WHERE id=%s
        """, (data_payload, result, cached["id"]))
    else:
        # Insert new
        cursor.execute("""
            INSERT INTO ai_results (child_id, module, data, result, created_at, updated_at)
            VALUES (%s, %s, %s, %s, NOW(), NOW())
        """, (child_id, module, data_payload, result))
```

### Cache Invalidation

**Automatic**:
- Triggered when `data_payload` changes
- Comparison done on every request

**Manual**:
- User clicks "Regenerate" button
- Passes `?regen=1` parameter
- Forces new AI call regardless of cache

```python
regen = request.args.get("regen")
use_cached = cached and cached["data"] == data_payload and not regen
```

---

## Security Implementation

### Input Validation

#### Email Validation
```python
EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")

if not EMAIL_REGEX.match(email):
    flash("Please enter a valid email address.", "warning")
```

#### Name Validation
```python
if not re.match(r'^[A-Za-z\s]+$', name):
    flash("Name must contain only alphabet letters.", "warning")
```

### SQL Injection Prevention

**Always use parameterized queries**:

```python
# ✅ CORRECT - Parameterized query
cursor.execute("SELECT * FROM users WHERE email = %s", (email,))

# ❌ INCORRECT - Vulnerable to SQL injection
cursor.execute(f"SELECT * FROM users WHERE email = '{email}'")
```

### CSRF Protection

Flask provides built-in CSRF protection through session cookies.

**Best Practices**:
- Use POST for state-changing operations
- Validate session tokens
- Set appropriate cookie flags

### XSS Prevention

**Template Escaping**:
Jinja2 auto-escapes by default:

```jinja
{{ user_input }}  {# Automatically escaped #}
{{ user_input|safe }}  {# Only use if you trust the input #}
```

**Safe HTML from AI**:
AI-generated HTML is marked safe only because:
- It comes from trusted AI source
- No user input is directly embedded
- HTML structure is controlled

```python
# In template
{{ benchmark_summary|safe }}
```

### Authorization Checks

**Child Ownership Validation**:
```python
cursor.execute("""
    SELECT * FROM children
    WHERE id=%s AND parent_id=%s
""", (child_id, current_user.id))

if not cursor.fetchone():
    flash("Access denied.", "danger")
    return redirect(url_for('profile'))
```

---

## API Reference

### Route Patterns

#### Authentication Routes
- `GET /register/select` - Account type selection
- `GET|POST /register/parent` - Parent registration
- `GET|POST /register/admin` - Admin registration (requires passkey)
- `GET|POST /login` - User authentication
- `GET /logout` - Session termination
- `GET|POST /forgot` - Password reset request
- `GET|POST /reset/<token>` - Password reset confirmation

#### Profile Management
- `GET|POST /profile` - User profile page
- `POST /profile/edit` - Update profile
- `POST /profile/change-password` - Change password
- `POST /profile/child/add` - Add child profile
- `POST /profile/child/edit/<child_id>` - Edit child
- `POST /profile/child/delete/<child_id>` - Delete child

#### Dashboard Routes
- `GET /dashboard` - Main dashboard
- `GET|POST /select-child` - Child selection

#### Preschool Tracker
- `GET|POST /dashboard/preschool` - Main preschool page
- `POST /dashboard/preschool/regenerate` - Regenerate AI analysis
- `POST /preschool/delete/<id>` - Delete milestone

#### Academic Progress
- `GET|POST /academic` - Academic tracking page
- `POST /academic/delete/<id>` - Delete academic record

#### Learning Style
- `GET|POST /dashboard/learning` - Learning style analyzer
- `GET /learning/test_questions/<test_id>` - Get test questions (JSON)
- `POST /learning/take_test/<child_id>` - Submit test
- `POST /learning/observation/submit/<child_id>` - Add observation
- `POST /learning/observation/delete/<observation_id>` - Delete observation

#### AI Modules
- `GET /dashboard/tutoring` - Tutoring recommendations
- `GET /dashboard/insights` - Academic insights
- `GET /dashboard/plan` - Personalized learning plan
- `GET /dashboard/resources` - Educational resources

#### Test Management
- `POST /add_test` - Create test
- `POST /tests/edit/<test_id>` - Edit test
- `POST /tests/delete/<test_id>` - Delete test

### Response Formats

#### HTML Responses
Most routes return rendered HTML templates.

#### JSON Responses
AJAX endpoints return JSON:

```python
# Success response
return jsonify({
    "success": True,
    "benchmark_summary": result,
    "last_generated": timestamp
})

# Error response
return jsonify({
    "error": "token_limit"
}), 429
```

### Request Methods

- `GET`: Retrieve/display data
- `POST`: Create/update/delete data

---

## Development Guide

### Setting Up Development Environment

1. **Clone Repository**:
```bash
git clone https://github.com/TongYwen/childfyp3.git
cd childfyp3
```

2. **Create Virtual Environment**:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install Dependencies**:
```bash
pip install -r requirements.txt
```

4. **Configure Environment**:
```bash
cp .env.txt .env
# Edit .env with your credentials
```

5. **Setup Database**:
```bash
mysql -u root -p < database_schema.sql
```

6. **Run Development Server**:
```bash
python app.py
```

Application runs on `http://127.0.0.1:5000`

### Adding a New AI Module

1. **Create Database Entry Point**:
```python
@app.route("/dashboard/new_module")
@login_required
def new_module():
    child_id = session.get("selected_child")
    # ... fetch data ...
```

2. **Implement Caching Logic**:
```python
# Prepare payload
data_payload = json.dumps(input_data, default=str)

# Check cache
cursor.execute("""
    SELECT * FROM ai_results
    WHERE child_id=%s AND module='new_module'
""", (child_id,))
cached = cursor.fetchone()

use_cached = cached and cached["data"] == data_payload
```

3. **Call Gemini API**:
```python
if not use_cached:
    prompt = f"""Your prompt here..."""

    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)
    result = response.text.strip()

    # Cache result
    if cached:
        cursor.execute("UPDATE ai_results SET ...")
    else:
        cursor.execute("INSERT INTO ai_results ...")
```

4. **Create Template**:
```html
<!-- templates/dashboard/_new_module.html -->
{% extends "dashboard.html" %}

{% block dashboard_content %}
<h2>New Module</h2>
<div>{{ result|safe }}</div>

<button onclick="regenerate()">Regenerate</button>
{% endblock %}
```

5. **Add Navigation Link**:
```html
<!-- In base.html or dashboard.html -->
<a href="{{ url_for('new_module') }}">New Module</a>
```

### Code Style Guidelines

**Python (PEP 8)**:
- 4 spaces for indentation
- Max line length: 100 characters
- Docstrings for functions
- Type hints where appropriate

```python
def calculate_age_months(dob: date, current_date: date) -> int:
    """
    Calculate age in months between two dates.

    Args:
        dob: Date of birth
        current_date: Current date

    Returns:
        Age in months
    """
    return (current_date.year - dob.year) * 12 + (current_date.month - dob.month)
```

**JavaScript**:
- ES6+ syntax
- Const/let instead of var
- Meaningful variable names
- Comments for complex logic

**HTML/Jinja2**:
- Proper indentation
- Semantic HTML5 tags
- Bootstrap classes for styling

### Debugging

**Enable Debug Mode**:
```python
# In .env
FLASK_DEBUG=True
```

**Flask Debug Toolbar** (optional):
```bash
pip install flask-debugtoolbar
```

```python
# In app.py
from flask_debugtoolbar import DebugToolbarExtension
toolbar = DebugToolbarExtension(app)
```

**Logging**:
```python
import logging

logging.basicConfig(level=logging.DEBUG)
app.logger.debug("Debug message")
app.logger.info("Info message")
app.logger.error("Error message")
```

---

## Deployment Guide

### Production Checklist

- [ ] Set `FLASK_DEBUG=False`
- [ ] Use production WSGI server (Gunicorn/uWSGI)
- [ ] Configure HTTPS with SSL certificate
- [ ] Set strong `SECRET_KEY`
- [ ] Change `ADMIN_PASSKEY`
- [ ] Use production database credentials
- [ ] Enable database connection pooling
- [ ] Set up logging and monitoring
- [ ] Configure firewall rules
- [ ] Regular database backups
- [ ] Rate limiting for API endpoints

### Using Gunicorn

1. **Install Gunicorn**:
```bash
pip install gunicorn
```

2. **Run Application**:
```bash
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

3. **Systemd Service** (Linux):
```ini
[Unit]
Description=Preschool Tracker
After=network.target

[Service]
User=www-data
WorkingDirectory=/path/to/app
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/gunicorn -w 4 -b 127.0.0.1:8000 app:app

[Install]
WantedBy=multi-user.target
```

### Nginx Configuration

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static {
        alias /path/to/app/static;
        expires 30d;
    }
}
```

---

## Testing

### Unit Testing

```python
import unittest
from app import app, is_strong_password

class TestPasswordValidation(unittest.TestCase):
    def test_strong_password(self):
        self.assertTrue(is_strong_password("MyPass123!"))

    def test_weak_password(self):
        self.assertFalse(is_strong_password("password"))

    def test_short_password(self):
        self.assertFalse(is_strong_password("Pass1!"))

if __name__ == '__main__':
    unittest.main()
```

### Integration Testing

```python
class TestAuthRoutes(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_login_page(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_invalid_login(self):
        response = self.app.post('/login', data={
            'email': 'test@example.com',
            'password': 'wrongpass'
        }, follow_redirects=True)
        self.assertIn(b'Invalid credentials', response.data)
```

---

## Performance Optimization

### Database Optimization
- Proper indexing on frequently queried columns
- Connection pooling for concurrent requests
- Query optimization (avoid N+1 queries)

### Caching
- AI result caching (implemented)
- Consider Redis for session storage
- CDN for static assets

### Frontend Optimization
- Minify CSS/JavaScript
- Lazy loading for images
- Asynchronous loading for non-critical resources

---

## Future Technical Enhancements

- [ ] REST API with authentication tokens
- [ ] WebSocket support for real-time updates
- [ ] Redis caching layer
- [ ] Elasticsearch for advanced search
- [ ] Docker containerization
- [ ] CI/CD pipeline
- [ ] Automated testing suite
- [ ] API documentation (Swagger/OpenAPI)
- [ ] GraphQL endpoint option
- [ ] Microservices architecture for scalability

---

**Document Version**: 1.0
**Last Updated**: November 2024
**Maintainer**: Development Team

