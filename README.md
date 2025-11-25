# Preschool Performance Tracker and Learning Style Analyzer

A comprehensive web-based application designed to help parents and educators track preschool children's development, academic progress, and learning styles using AI-powered insights.

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage Guide](#usage-guide)
- [AI Features](#ai-features)
- [Database Schema](#database-schema)
- [Security Features](#security-features)
- [Contributing](#contributing)
- [License](#license)

## Overview

The Preschool Performance Tracker and Learning Style Analyzer is an intelligent educational platform that combines developmental milestone tracking, academic performance monitoring, and AI-powered analysis to provide personalized insights and recommendations for preschool children's learning journey.

### Purpose

- **Track Development**: Monitor preschool milestones across multiple developmental domains
- **Academic Progress**: Record and analyze subject-specific performance over time
- **Learning Styles**: Identify individual learning preferences through observations and custom tests
- **Personalized Recommendations**: Generate AI-powered tutoring suggestions and learning plans
- **Resource Discovery**: Get curated educational materials tailored to each child's needs

## Key Features

### 1. User Management
- **Dual Role System**: Separate registration for Parents and Administrators
- **Secure Authentication**: Password hashing with bcrypt, email validation
- **Password Recovery**: Email-based password reset with time-limited tokens
- **Admin Passkey**: Additional security layer for administrator registration

### 2. Child Profile Management
- Create and manage multiple child profiles per parent account
- Track essential information: name, date of birth, age, grade level, gender
- Add custom notes and observations
- Switch between children seamlessly

### 3. Preschool Milestone Tracker
- Record developmental achievements across key domains:
  - Physical Development
  - Cognitive Development
  - Social-Emotional Development
  - Language Development
  - Motor Skills
- Age-based milestone tracking (calculated in months)
- Compare against standardized developmental benchmarks
- AI-powered developmental progress analysis

### 4. Academic Progress Monitoring
- Track subject-specific scores over time
- Support for multiple subjects (Math, English, Science, etc.)
- Custom subject support
- Visual progress tracking by month/year
- Historical performance data retention

### 5. Learning Style Analyzer
- **Observation System**: Record behavioral and learning observations
- **Custom Tests**: Create and administer personalized assessment tests
- **Test Types**: Support for text responses and scaled answers (1-5)
- **AI Analysis**: Identify learning style preferences:
  - Visual learners
  - Auditory learners
  - Reading/Writing learners
  - Kinesthetic learners
  - Mixed learning styles
- Actionable suggestions for parents

### 6. AI-Powered Insights
Leveraging Google Gemini AI for intelligent analysis:
- **Preschool Analysis**: Compare milestones against age-based benchmarks
- **Learning Style Detection**: Analyze observations and test results
- **Academic Insights**: Identify strengths and areas for improvement
- **Tutoring Recommendations**: Personalized support suggestions
- **Learning Plans**: Weekly activity schedules with daily recommendations
- **Resource Hub**: Curated educational materials (videos, games, books)

### 7. Smart Caching System
- Efficient AI result caching to minimize API costs
- Automatic cache invalidation on data changes
- Manual regeneration option for fresh insights
- Timestamp tracking for cache freshness

### 8. Dashboard & Visualization
- Centralized child dashboard with all insights
- Quick access to all tracking modules
- Summary views of AI analysis results
- Recent activity tracking

## Technology Stack

### Backend
- **Framework**: Flask (Python web framework)
- **Database**: MySQL
- **Authentication**: Flask-Login, Flask-Bcrypt
- **Email**: Flask-Mail (for password reset functionality)
- **AI/ML**: Google Gemini 2.5 Flash API
- **Data Processing**: Pandas (for benchmark data handling)

### Frontend
- **Templating**: Jinja2 (Flask templates)
- **Styling**: Bootstrap 5 (responsive design)
- **JavaScript**: Vanilla JS for dynamic interactions

### Security
- Password hashing with bcrypt
- Session management with Flask-Login
- CSRF protection
- SQL injection prevention (parameterized queries)
- Email validation with regex
- Strong password requirements

## Installation

### Prerequisites
- Python 3.8 or higher
- MySQL 5.7 or higher
- pip (Python package manager)
- A Google API key for Gemini AI

### Step 1: Clone the Repository
```bash
git clone https://github.com/TongYwen/childfyp3.git
cd childfyp3
```

### Step 2: Create Virtual Environment
```bash
python -m venv .venv

# On Windows
.venv\Scripts\activate

# On macOS/Linux
source .venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Database Setup
1. Open MySQL and create a database:
```sql
CREATE DATABASE childgrowth_insights;
```

2. Import the database schema (if Dump20250917.sql exists):
```bash
mysql -u your_username -p childgrowth_insights < Dump20250917.sql
```

Or create tables manually using the schema in [Database Schema](#database-schema) section.

### Step 5: Configure Environment Variables
Create a `.env` file in the project root:
```env
# Database Configuration
DB_HOST=localhost
DB_USER=your_mysql_username
DB_PASS=your_mysql_password
DB_NAME=childgrowth_insights

# Flask Configuration
SECRET_KEY=your_secret_key_here
FLASK_DEBUG=True

# Email Configuration (for password reset)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password

# Google Gemini AI
GOOGLE_API_KEY=your_gemini_api_key
```

**Important**: For Gmail, use an [App Password](https://myaccount.google.com/apppasswords), not your regular password.

### Step 6: Prepare Benchmark Data
Ensure the developmental milestones CSV file exists:
```bash
mkdir -p static/data
# Place your developmental_milestones.csv in static/data/
```

### Step 7: Run the Application
```bash
python app.py
```

The application will be available at `http://127.0.0.1:5000`

## Configuration

### Email Setup
The application uses email for password reset functionality. Configure your email settings in `.env`:

1. **Gmail Users**:
   - Enable 2-factor authentication
   - Generate an App Password at https://myaccount.google.com/apppasswords
   - Use the 16-character app password in `.env`

2. **Other Email Providers**:
   - Update `MAIL_SERVER` and `MAIL_PORT` accordingly
   - Adjust `MAIL_USE_TLS` or `MAIL_USE_SSL` as needed

### Admin Passkey
The admin registration passkey is set in `app.py`:
```python
ADMIN_PASSKEY = "child1234"
```
Change this to a secure passkey in production.

### Google Gemini API
1. Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Add it to your `.env` file as `GOOGLE_API_KEY`
3. Note: The free tier has rate limits

## Usage Guide

### For Parents

#### 1. Registration
1. Navigate to the registration page
2. Choose "Parent Account"
3. Fill in your details:
   - Full name (letters only)
   - Valid email address
   - Strong password (8+ characters, uppercase, lowercase, symbol)
4. Confirm your password
5. Click "Register"

#### 2. Adding a Child
1. Log in to your account
2. Go to "Profile" section
3. Click "Add Child Profile"
4. Enter child information:
   - Name
   - Date of birth
   - Current age
   - Grade level
   - Gender
   - Optional notes
5. Save the profile

#### 3. Tracking Preschool Milestones
1. Select a child from the dashboard
2. Navigate to "Preschool Tracker"
3. Click "Add Milestone"
4. Select developmental domain
5. Describe the milestone achieved
6. Set the date (month/year)
7. View AI analysis comparing to benchmarks

#### 4. Recording Academic Progress
1. Go to "Academic Progress"
2. Click "Add Record"
3. Select or enter subject name
4. Enter score
5. Set date (month/year)
6. View progress charts

#### 5. Analyzing Learning Style
1. Navigate to "Learning Style"
2. **Add Observations**:
   - Record behavioral observations
   - Note learning preferences
   - Document engagement patterns
3. **Create Custom Tests** (in Profile):
   - Design questions
   - Choose answer types (text or scale 1-5)
   - Save test template
4. **Take Tests**:
   - Select a test from dropdown
   - Answer all questions
   - Submit responses
5. View AI-generated learning style analysis

#### 6. Getting AI Insights
- **Dashboard Overview**: See summaries of all analyses
- **Tutoring Recommendations**: Get personalized support suggestions
- **Learning Plan**: Access weekly activity schedules
- **Resources Hub**: Discover curated educational materials
- **AI Insights**: View strengths and weakness analysis

#### 7. Regenerating Analysis
All AI modules have a "Regenerate" button to create fresh insights when data changes.

### For Administrators

#### 1. Registration
1. Choose "Administrator Account"
2. Enter the admin passkey (default: `child1234`)
3. Complete registration with secure credentials

#### 2. Admin Features
- Full access to all parent features
- Ability to create and manage tests
- Access to all child profiles
- System-wide data management

## AI Features

### 1. Preschool Development Analysis
**Module**: `preschool`

**Input**:
- Child's developmental milestones with age in months
- Benchmark dataset (CSV with age-based standards)

**Output**:
- Areas that are age-appropriate
- Areas showing developmental delays
- Areas where child is advanced
- Overall development progress summary

**Technology**: Google Gemini 2.5 Flash with custom prompt engineering

### 2. Learning Style Detection
**Module**: `learning`

**Input**:
- Parent observations
- Test answer responses (text and scaled)

**Output**:
- Identified learning style (Visual/Auditory/Reading-Writing/Kinesthetic/Mixed)
- Reasoning explanation (3-5 sentences)
- 3-5 actionable suggestions for parents

**Methodology**: Pattern analysis of behaviors and preferences

### 3. Academic Insights
**Module**: `insights`

**Input**:
- Subject-wise academic scores
- Historical performance data

**Output**:
- Key strengths identification
- Areas needing support
- Practical home-based suggestions
- Parent-friendly language (no exact scores mentioned)

### 4. Tutoring Recommendations
**Module**: `tutoring`

**Input**:
- Learning style analysis results
- Preschool development summary

**Output**:
- Identified weak areas requiring support
- Recommended subjects for tutoring
- Personalized activity suggestions
- Teaching style recommendations

### 5. Personalized Learning Plan
**Module**: `learning_plan`

**Input**:
- Academic scores
- Learning style analysis
- Preschool development data
- Tutoring recommendations

**Output**:
- Learning plan summary
- Weekly activity schedule (Monday-Sunday)
- 2-4 activities per day (10-20 minutes each)
- Long-term strategy points
- Activities aligned with learning style

### 6. Educational Resources Hub
**Module**: `resources`

**Input**:
- Academic performance
- Learning style preferences
- Child's age and grade level

**Output**:
- Curated video recommendations
- Educational games and apps
- Book and reading material suggestions
- Age-appropriate, skill-targeted resources

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('parent', 'admin') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Children Table
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
    FOREIGN KEY (parent_id) REFERENCES users(id) ON DELETE CASCADE
);
```

### Preschool Assessments Table
```sql
CREATE TABLE preschool_assessments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    child_id INT NOT NULL,
    domain VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (child_id) REFERENCES children(id) ON DELETE CASCADE
);
```

### Academic Scores Table
```sql
CREATE TABLE academic_scores (
    id INT PRIMARY KEY AUTO_INCREMENT,
    child_id INT NOT NULL,
    subject VARCHAR(100) NOT NULL,
    score INT NOT NULL,
    date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (child_id) REFERENCES children(id) ON DELETE CASCADE
);
```

### Tests Table
```sql
CREATE TABLE tests (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    name VARCHAR(200) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

### Test Questions Table
```sql
CREATE TABLE test_questions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    test_id INT NOT NULL,
    question TEXT NOT NULL,
    answer_type ENUM('text', 'scale') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (test_id) REFERENCES tests(id) ON DELETE CASCADE
);
```

### Test Answers Table
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
    FOREIGN KEY (question_id) REFERENCES test_questions(id) ON DELETE CASCADE
);
```

### Learning Observations Table
```sql
CREATE TABLE learning_observations (
    id INT PRIMARY KEY AUTO_INCREMENT,
    child_id INT NOT NULL,
    observation TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (child_id) REFERENCES children(id) ON DELETE CASCADE
);
```

### AI Results Table
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
    UNIQUE KEY unique_child_module (child_id, module)
);
```

## Security Features

### Authentication & Authorization
- Role-based access control (Parent/Admin)
- Session-based authentication with Flask-Login
- Secure password hashing with bcrypt (cost factor 12)
- Child profile ownership validation

### Password Security
- Minimum 8 characters
- Must include uppercase letter
- Must include lowercase letter
- Must include special character
- Password strength validation on registration

### Data Protection
- Parameterized SQL queries prevent injection attacks
- CSRF protection enabled
- XSS prevention through template escaping
- Email validation with regex
- Name validation (alphabetic characters only)

### Email Security
- Time-limited password reset tokens (1 hour expiry)
- URLSafeTimedSerializer for token generation
- Tokens salted with 'password-reset-salt'
- HTML email templates for professional appearance

## File Structure

```
childfyp3/
├── app.py                          # Main application file
├── config.py                       # Configuration classes
├── requirements.txt                # Python dependencies
├── .env                            # Environment variables (not in repo)
├── README.md                       # This file
├── static/
│   ├── data/
│   │   └── developmental_milestones.csv
│   ├── style.css                   # Custom styles
│   ├── logo.png
│   ├── logo_words.png
│   ├── background-1.jpg
│   ├── register-background.jpg
│   ├── select-child-bg.jpg
│   └── select-child.png
├── templates/
│   ├── base.html                   # Base template with navbar
│   ├── login.html
│   ├── register_select.html
│   ├── register_parent.html
│   ├── register_admin.html
│   ├── forgot.html
│   ├── reset.html
│   ├── profile.html
│   ├── select_child.html
│   ├── dashboard.html              # Main dashboard layout
│   └── dashboard/
│       ├── _dashboard.html         # Dashboard overview
│       ├── _preschool.html         # Preschool tracker
│       ├── _academic.html          # Academic progress
│       ├── _learning.html          # Learning style analyzer
│       ├── _tutoring.html          # Tutoring recommendations
│       ├── _insights.html          # AI insights
│       ├── _plan.html              # Learning plan
│       └── _resources.html         # Resources hub
└── __pycache__/                    # Python cache (ignored)
```

## API Endpoints

### Authentication
- `GET /register/select` - Choose account type
- `GET/POST /register/parent` - Parent registration
- `GET/POST /register/admin` - Admin registration
- `GET/POST /login` - User login
- `GET /logout` - User logout
- `GET/POST /forgot` - Password reset request
- `GET/POST /reset/<token>` - Password reset with token

### Profile Management
- `GET/POST /profile` - View and edit user profile
- `POST /profile/edit` - Update user information
- `POST /profile/change-password` - Change password
- `POST /profile/child/add` - Add child profile
- `POST /profile/child/edit/<child_id>` - Edit child profile
- `POST /profile/child/delete/<child_id>` - Delete child profile

### Child Selection
- `GET/POST /select-child` - Select active child for session

### Tests Management
- `POST /add_test` - Create new test
- `POST /tests/edit/<test_id>` - Edit existing test
- `POST /tests/delete/<test_id>` - Delete test

### Dashboard & Modules
- `GET /dashboard` - Main dashboard
- `GET/POST /dashboard/preschool` - Preschool tracker
- `POST /dashboard/preschool/regenerate` - Regenerate AI analysis
- `POST /preschool/delete/<id>` - Delete preschool record
- `GET/POST /academic` - Academic progress
- `POST /academic/delete/<id>` - Delete academic record
- `GET/POST /dashboard/learning` - Learning style analyzer
- `GET /learning/test_questions/<test_id>` - Get test questions (AJAX)
- `POST /learning/take_test/<child_id>` - Submit test answers
- `POST /learning/observation/submit/<child_id>` - Add observation
- `POST /learning/observation/delete/<observation_id>` - Delete observation
- `GET /dashboard/tutoring` - Tutoring recommendations
- `GET /dashboard/insights` - AI insights
- `GET /dashboard/plan` - Personalized learning plan
- `GET /dashboard/resources` - Educational resources hub

### Root
- `GET /` - Redirects to dashboard (if logged in) or login

## Troubleshooting

### Common Issues

#### 1. Database Connection Errors
```
Error: Can't connect to MySQL server
```
**Solution**:
- Verify MySQL is running
- Check DB credentials in `.env`
- Ensure database exists
- Verify user has proper permissions

#### 2. Email Sending Failures
```
Error: SMTP authentication error
```
**Solution**:
- Use Gmail App Password, not regular password
- Enable 2-factor authentication first
- Check MAIL_SERVER and MAIL_PORT settings
- Verify email credentials in `.env`

#### 3. Gemini AI Errors
```
Error: 429 quota exceeded / token limit
```
**Solution**:
- Check your API key is valid
- Monitor your API usage quota
- Wait for quota reset (free tier limits)
- Consider upgrading to paid tier

#### 4. Missing Benchmark Data
```
FileNotFoundError: developmental_milestones.csv
```
**Solution**:
- Ensure CSV file exists in `static/data/`
- Check file permissions
- Verify CSV format and headers

#### 5. Template Not Found Errors
**Solution**:
- Verify all templates exist in `templates/` directory
- Check dashboard partials in `templates/dashboard/`
- Ensure file names match references in `app.py`

## Best Practices

### For Development
1. Always use virtual environment
2. Never commit `.env` file
3. Keep `SECRET_KEY` secure and random
4. Use strong admin passkey in production
5. Enable debug mode only in development
6. Regularly backup your database

### For Production
1. Set `FLASK_DEBUG=False`
2. Use a production WSGI server (Gunicorn, uWSGI)
3. Enable HTTPS with SSL certificates
4. Use environment-specific configurations
5. Implement rate limiting for API calls
6. Set up logging and monitoring
7. Regular security audits
8. Database connection pooling

### For Users
1. Use valid email addresses for account recovery
2. Create strong, unique passwords
3. Keep child information up-to-date
4. Regularly track milestones and progress
5. Review AI insights periodically
6. Use the regenerate feature when data changes significantly

## Future Enhancements

- [ ] Multi-language support (Bahasa Malaysia, Chinese)
- [ ] Mobile app version (React Native/Flutter)
- [ ] Parent-teacher collaboration features
- [ ] Progress reports export (PDF)
- [ ] Data visualization dashboards
- [ ] Push notifications for milestone tracking
- [ ] Integration with educational APIs
- [ ] Social features (parent community)
- [ ] Advanced analytics and predictive modeling
- [ ] Video upload for milestone documentation

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add comments for complex logic
- Write docstrings for functions
- Keep functions focused and modular

## License

This project is developed for educational purposes as part of a Final Year Project (FYP).

## Support

For issues, questions, or suggestions:
- Create an issue on GitHub
- Contact the development team
- Check the troubleshooting section

## Acknowledgments

- Google Gemini AI for intelligent analysis capabilities
- Flask community for excellent documentation
- Bootstrap for responsive UI components
- Early childhood development researchers for benchmark data

---

**Version**: 1.0.0
**Last Updated**: November 2024
**Developed by**: TongYwen
**Institution**: [Your Institution Name]

