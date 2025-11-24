"""
Test data fixtures for ChildGrowth Insights tests.
Contains sample data used across multiple test files.
"""
from datetime import date, datetime


# Sample Users
SAMPLE_USERS = {
    'parent': {
        'id': 1,
        'name': 'John Parent',
        'email': 'john.parent@example.com',
        'password': 'SecurePass123!',
        'hashed_password': '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.G9P5z5z5z5z5z5',
        'role': 'parent'
    },
    'admin': {
        'id': 2,
        'name': 'Admin User',
        'email': 'admin@example.com',
        'password': 'AdminPass123!',
        'hashed_password': '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.G9P5z5z5z5z5z5',
        'role': 'admin'
    },
    'parent2': {
        'id': 3,
        'name': 'Jane Parent',
        'email': 'jane.parent@example.com',
        'password': 'JanePass123!',
        'hashed_password': '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.G9P5z5z5z5z5z5',
        'role': 'parent'
    }
}

# Sample Children
SAMPLE_CHILDREN = {
    'toddler': {
        'id': 1,
        'name': 'Emma Smith',
        'dob': date(2022, 3, 15),
        'gender': 'female',
        'user_id': 1
    },
    'preschooler': {
        'id': 2,
        'name': 'Liam Smith',
        'dob': date(2020, 8, 22),
        'gender': 'male',
        'user_id': 1
    },
    'school_age': {
        'id': 3,
        'name': 'Olivia Johnson',
        'dob': date(2017, 11, 5),
        'gender': 'female',
        'user_id': 3
    }
}

# Sample Academic Records
SAMPLE_ACADEMIC_RECORDS = [
    {
        'id': 1,
        'child_id': 3,
        'subject': 'Mathematics',
        'score': 85,
        'date': date(2024, 1, 15)
    },
    {
        'id': 2,
        'child_id': 3,
        'subject': 'English',
        'score': 92,
        'date': date(2024, 1, 15)
    },
    {
        'id': 3,
        'child_id': 3,
        'subject': 'Science',
        'score': 78,
        'date': date(2024, 1, 15)
    },
    {
        'id': 4,
        'child_id': 3,
        'subject': 'Mathematics',
        'score': 88,
        'date': date(2024, 2, 15)
    }
]

# Sample Developmental Milestones
SAMPLE_MILESTONES = [
    {
        'id': 1,
        'child_id': 1,
        'category': 'Motor',
        'milestone': 'Walking independently',
        'achieved': True,
        'achieved_date': date(2023, 6, 1)
    },
    {
        'id': 2,
        'child_id': 1,
        'category': 'Language',
        'milestone': 'First words',
        'achieved': True,
        'achieved_date': date(2023, 3, 15)
    },
    {
        'id': 3,
        'child_id': 1,
        'category': 'Social',
        'milestone': 'Plays alongside other children',
        'achieved': False,
        'achieved_date': None
    }
]

# Sample Learning Observations
SAMPLE_LEARNING_OBSERVATIONS = [
    {
        'id': 1,
        'child_id': 2,
        'observation': 'Shows strong interest in building blocks and construction toys',
        'learning_style': 'kinesthetic',
        'date': date(2024, 1, 10)
    },
    {
        'id': 2,
        'child_id': 2,
        'observation': 'Prefers visual aids when learning new concepts',
        'learning_style': 'visual',
        'date': date(2024, 1, 20)
    },
    {
        'id': 3,
        'child_id': 2,
        'observation': 'Enjoys listening to stories and audio books',
        'learning_style': 'auditory',
        'date': date(2024, 2, 5)
    }
]

# Sample Test Questions
SAMPLE_TEST_QUESTIONS = [
    {
        'id': 1,
        'test_id': 1,
        'question': 'When learning something new, I prefer to...',
        'options': ['Watch a demonstration', 'Listen to an explanation', 'Try it myself', 'Read about it'],
        'category': 'learning_preference'
    },
    {
        'id': 2,
        'test_id': 1,
        'question': 'I remember information best when I...',
        'options': ['See it written down', 'Hear it spoken', 'Practice doing it', 'Discuss it with others'],
        'category': 'memory_style'
    }
]

# Sample AI Responses
SAMPLE_AI_RESPONSES = {
    'preschool_analysis': """
Based on Emma's developmental profile:

**Strengths:**
- Strong motor development for age
- Good social engagement
- On track with language milestones

**Areas for Growth:**
- Continue encouraging social play
- Introduce more complex fine motor activities

**Recommendations:**
1. Provide opportunities for peer interaction
2. Engage in arts and crafts activities
3. Read together daily to support language development
""",
    'tutoring_recommendation': """
Based on Olivia's academic performance:

**Mathematics (85%):**
- Consider visual aids for problem-solving
- Practice with real-world math scenarios

**English (92%):**
- Continue creative writing exercises
- Introduce more challenging reading material

**Science (78%):**
- Focus on hands-on experiments
- Connect concepts to everyday observations
""",
    'learning_plan': """
**Personalized Learning Plan for Liam:**

**Week 1-2:** Focus on kinesthetic learning activities
- Building projects
- Outdoor exploration
- Hands-on science experiments

**Week 3-4:** Introduce visual learning components
- Educational videos
- Picture books
- Visual schedules

**Ongoing:** Balance of all learning styles with emphasis on strengths
"""
}

# Test Subject List
SUBJECTS = [
    'Mathematics',
    'English',
    'Science',
    'Social Studies',
    'Art',
    'Music',
    'Physical Education'
]

# Test Score Ranges
SCORE_RANGES = {
    'excellent': (90, 100),
    'good': (80, 89),
    'average': (70, 79),
    'below_average': (60, 69),
    'needs_improvement': (0, 59)
}

# Age Ranges (in months)
AGE_RANGES = {
    'infant': (0, 12),
    'toddler': (12, 36),
    'preschool': (36, 60),
    'school_age': (60, 144)
}

# Learning Styles
LEARNING_STYLES = ['visual', 'auditory', 'kinesthetic', 'reading_writing']

# Developmental Categories
DEVELOPMENTAL_CATEGORIES = [
    'Motor',
    'Language',
    'Social',
    'Cognitive',
    'Emotional',
    'Self-Help'
]
