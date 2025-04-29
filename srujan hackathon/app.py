import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import google.generativeai as genai
from dotenv import load_dotenv
import os
import json
import matplotlib.pyplot as plt
import time
import altair as alt
from PIL import Image
from io import BytesIO
import requests
import random
import uuid
import tempfile
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

# Initialize session state variables
if 'profile' not in st.session_state:
    st.session_state.profile = {
        'name': '',
        'interests': '',
        'learning_style': '',
        'career_goal': '',
        'experience_level': 'Beginner',
        'completed_courses': []
    }

if 'recommended_courses' not in st.session_state:
    st.session_state.recommended_courses = None

if 'courses_df' not in st.session_state:
    # Initialize the courses DataFrame with all required columns and meaningful course names
    courses_df = pd.DataFrame({
        'course_id': range(1, 21),
        'title': [
            'Introduction to Python Programming',
            'Data Structures and Algorithms',
            'Web Development Fundamentals',
            'Machine Learning Basics',
            'Database Management Systems',
            'Software Engineering Principles',
            'Artificial Intelligence Fundamentals',
            'Cloud Computing Essentials',
            'Cybersecurity Basics',
            'Mobile App Development',
            'Advanced Data Science',
            'DevOps Engineering',
            'Blockchain Development',
            'UI/UX Design Principles',
            'Natural Language Processing',
            'Computer Vision Fundamentals',
            'Quantum Computing Basics',
            'Internet of Things (IoT)',
            'Game Development Foundations',
            'Augmented Reality Development'
        ],
        'description': [
            'Learn Python programming fundamentals and basic syntax',
            'Study fundamental data structures and algorithm design',
            'Build responsive websites using HTML, CSS, and JavaScript',
            'Introduction to machine learning concepts and techniques',
            'Learn database design and SQL fundamentals',
            'Study software development lifecycle and best practices',
            'Explore AI concepts and applications',
            'Learn cloud platforms and services',
            'Understanding cybersecurity principles and practices',
            'Develop mobile applications for iOS and Android',
            'Advanced topics in data science and analytics',
            'Learn DevOps practices and tools',
            'Blockchain technology and smart contracts',
            'Design user interfaces and experiences',
            'Process and analyze natural language',
            'Computer vision algorithms and applications',
            'Introduction to quantum computing concepts',
            'Connected devices and IoT platforms',
            'Game design and development basics',
            'AR development and 3D modeling'
        ],
        'difficulty': [
            'Beginner', 'Intermediate', 'Beginner', 'Intermediate',
            'Beginner', 'Intermediate', 'Intermediate', 'Intermediate',
            'Beginner', 'Intermediate', 'Advanced', 'Advanced',
            'Advanced', 'Beginner', 'Advanced', 'Advanced',
            'Advanced', 'Intermediate', 'Beginner', 'Advanced'
        ],
        'category': [
            'Programming', 'Computer Science', 'Web Development', 'Machine Learning',
            'Databases', 'Software Engineering', 'Artificial Intelligence', 'Cloud Computing',
            'Security', 'Mobile Development', 'Data Science', 'DevOps',
            'Blockchain', 'Design', 'AI/ML', 'Computer Vision',
            'Quantum Computing', 'IoT', 'Game Development', 'AR/VR'
        ],
        'duration_weeks': [
            4, 6, 4, 8,
            4, 6, 8, 6,
            4, 8, 10, 8,
            8, 4, 8, 8,
            10, 6, 6, 8
        ],
        'skills_gained': [
            ['Python', 'Programming Basics', 'Problem Solving'],
            ['Data Structures', 'Algorithms', 'Python'],
            ['HTML', 'CSS', 'JavaScript'],
            ['Python', 'ML Algorithms', 'Data Analysis'],
            ['SQL', 'Database Design', 'Data Modeling'],
            ['Git', 'Agile', 'Software Architecture'],
            ['AI Algorithms', 'Python', 'Neural Networks'],
            ['AWS', 'Azure', 'Cloud Architecture'],
            ['Security Protocols', 'Cryptography', 'Network Security'],
            ['Swift', 'Kotlin', 'Mobile UI Design'],
            ['Advanced Python', 'Big Data', 'Statistical Analysis'],
            ['Docker', 'Kubernetes', 'CI/CD'],
            ['Solidity', 'Smart Contracts', 'Cryptography'],
            ['UI Design', 'UX Research', 'Prototyping'],
            ['NLP', 'Text Analytics', 'Machine Learning'],
            ['OpenCV', 'Image Processing', 'Deep Learning'],
            ['Quantum Algorithms', 'Q#', 'Linear Algebra'],
            ['Embedded Systems', 'Sensors', 'IoT Protocols'],
            ['Unity', 'C#', 'Game Design'],
            ['Unity AR', 'ARKit', 'ARCore']
        ],
        'career_relevance': [
            ['Software Developer', 'Python Developer'],
            ['Software Engineer', 'Algorithm Engineer'],
            ['Web Developer', 'Frontend Developer'],
            ['Machine Learning Engineer', 'Data Scientist'],
            ['Database Administrator', 'Data Engineer'],
            ['Software Architect', 'Project Manager'],
            ['AI Engineer', 'Research Scientist'],
            ['Cloud Engineer', 'Solutions Architect'],
            ['Security Engineer', 'Security Analyst'],
            ['Mobile Developer', 'iOS/Android Developer'],
            ['Data Scientist', 'Analytics Manager'],
            ['DevOps Engineer', 'Site Reliability Engineer'],
            ['Blockchain Developer', 'Smart Contract Engineer'],
            ['UI/UX Designer', 'Product Designer'],
            ['NLP Engineer', 'AI Researcher'],
            ['Computer Vision Engineer', 'AI Developer'],
            ['Quantum Computing Researcher', 'Quantum Engineer'],
            ['IoT Engineer', 'Embedded Systems Developer'],
            ['Game Developer', 'Unity Developer'],
            ['AR Developer', 'Mixed Reality Engineer']
        ],
        'prerequisites': [
            ['None'],
            ['Introduction to Python Programming'],
            ['None'],
            ['Introduction to Python Programming'],
            ['None'],
            ['Introduction to Python Programming'],
            ['Machine Learning Basics'],
            ['None'],
            ['None'],
            ['Web Development Fundamentals'],
            ['Machine Learning Basics', 'Data Structures and Algorithms'],
            ['Cloud Computing Essentials'],
            ['Web Development Fundamentals'],
            ['None'],
            ['Machine Learning Basics', 'Python Programming'],
            ['Machine Learning Basics', 'Python Programming'],
            ['Machine Learning Basics'],
            ['Introduction to Python Programming'],
            ['None'],
            ['Mobile App Development']
        ]
    })
    st.session_state.courses_df = courses_df

# Access the courses DataFrame
courses_df = st.session_state.courses_df

# Define hours per week based on difficulty level
hours_per_week = {
    'Beginner': 5,
    'Intermediate': 8,
    'Advanced': 12
}

# Learning styles characteristics
learning_styles_characteristics = {
    'Visual': {
        'description': 'You learn best through visual aids like diagrams, charts, and videos.',
        'preferred_methods': [
            'Video tutorials',
            'Infographics',
            'Mind maps',
            'Visual documentation'
        ],
        'study_tips': [
            'Use color coding in your notes',
            'Create mind maps for complex topics',
            'Watch video tutorials',
            'Draw diagrams and flowcharts'
        ]
    },
    'Auditory': {
        'description': 'You learn best through listening and verbal communication.',
        'preferred_methods': [
            'Video lectures',
            'Group discussions',
            'Audio books',
            'Verbal explanations'
        ],
        'study_tips': [
            'Record and listen to lectures',
            'Participate in group discussions',
            'Use text-to-speech for reading',
            'Explain concepts out loud'
        ]
    },
    'Reading/Writing': {
        'description': 'You learn best through reading and writing text.',
        'preferred_methods': [
            'Written tutorials',
            'Documentation',
            'Taking notes',
            'Text-based resources'
        ],
        'study_tips': [
            'Take detailed notes',
            'Read documentation thoroughly',
            'Write summaries of concepts',
            'Create written study guides'
        ]
    },
    'Kinesthetic': {
        'description': 'You learn best through hands-on practice and experience.',
        'preferred_methods': [
            'Practical exercises',
            'Coding projects',
            'Interactive tutorials',
            'Learning by doing'
        ],
        'study_tips': [
            'Practice with hands-on exercises',
            'Build small projects',
            'Use interactive tutorials',
            'Take frequent practice breaks'
        ]
    }
}

# Load environment variables
load_dotenv()

# Configure Gemini API
api_key = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=api_key)

# Initialize Gemini model
model = genai.GenerativeModel('gemini-2.0-flash')

# Set page configuration
st.set_page_config(
    page_title="EduPathfinder | Personalized Learning Journey",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add global styles for better visibility
st.markdown("""
<style>
    /* Base styles */
    .main {
        background-color: #ffffff;
        color: #6a1b9a !important;
    }

    /* Text styles */
    p, li, label, span {
        color: #6a1b9a !important;
        font-size: 16px !important;
    }

    h1 {
        color: #4a148c !important;
        font-size: 32px !important;
        font-weight: bold !important;
    }

    h2 {
        color: #4a148c !important;
        font-size: 24px !important;
        font-weight: bold !important;
    }

    h3 {
        color: #4a148c !important;
        font-size: 20px !important;
        font-weight: bold !important;
    }

    /* Form fields */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > div,
    .stTextArea > div > div > textarea {
        color: #ffffff !important;
        font-size: 16px !important;
        background-color: #9c27b0 !important;
        border: 1px solid #ce93d8 !important;
        border-radius: 5px !important;
        padding: 8px 12px !important;
    }

    /* Selectbox specific styles */
    .stSelectbox > div > div > div {
        background-color: #9c27b0 !important;
        border-color: #ce93d8 !important;
        color: #ffffff !important;
    }

    .stSelectbox > div > div > div:hover {
        border-color: #ce93d8 !important;
        background-color: #7b1fa2 !important;
    }

    /* Dropdown options positioning and styling */
    .stSelectbox [data-baseweb="popover"] {
        position: absolute !important;
        top: 100% !important;
        left: 0 !important;
        margin-top: 4px !important;
    }

    /* Dropdown options */
    .stSelectbox [data-baseweb="select"] > div {
        background-color: #9c27b0 !important;
        border: 1px solid #ce93d8 !important;
        color: #ffffff !important;
    }

    .stSelectbox [data-baseweb="select"] ul {
        background-color: #9c27b0 !important;
        border: 1px solid #ce93d8 !important;
        box-shadow: 0 2px 5px rgba(156,39,176,0.2) !important;
        max-height: 300px !important;
        overflow-y: auto !important;
    }

    .stSelectbox [data-baseweb="select"] ul li {
        background-color: #9c27b0 !important;
        color: #ffffff !important;
        padding: 8px 12px !important;
    }

    .stSelectbox [data-baseweb="select"] ul li:hover {
        background-color: #7b1fa2 !important;
        color: #ffffff !important;
    }

    /* Selected option text color */
    .stSelectbox [data-baseweb="select"] span {
        color: #ffffff !important;
    }

    /* Dropdown arrow color */
    .stSelectbox [data-baseweb="select"] svg {
        fill: #ffffff !important;
    }

    /* Option highlight on hover/focus */
    .stSelectbox [data-baseweb="select"] [role="option"]:hover,
    .stSelectbox [data-baseweb="select"] [role="option"]:focus {
        background-color: #7b1fa2 !important;
        cursor: pointer !important;
    }

    /* Selected option in dropdown */
    .stSelectbox [data-baseweb="select"] [aria-selected="true"] {
        background-color: #7b1fa2 !important;
        color: #ffffff !important;
    }

    /* Form field focus states */
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > div:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #ce93d8 !important;
        box-shadow: 0 0 0 2px rgba(156,39,176,0.2) !important;
    }

    /* Select slider styles */
    .stSlider > div > div > div {
        background-color: #9c27b0 !important;
    }

    .stSlider > div > div > div > div {
        background-color: #6a1b9a !important;
    }

    /* Radio and checkbox styles */
    .stRadio > div,
    .stCheckbox > div {
        background-color: #f8f9fa !important;
        padding: 10px !important;
        border-radius: 5px !important;
        border: 1px solid #9c27b0 !important;
    }

    .stRadio label,
    .stCheckbox label {
        color: #6a1b9a !important;
        font-weight: 500 !important;
    }

    /* Label styles */
    .stMarkdown label {
        color: #6a1b9a !important;
        font-weight: 600 !important;
        margin-bottom: 5px !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        background-color: #f8f9fa;
    }

    .stTabs [data-baseweb="tab"] {
        color: #6a1b9a !important;
        font-size: 16px !important;
        font-weight: 500 !important;
        background-color: #f3e5f5;
        padding: 10px 20px;
        border-radius: 5px;
    }

    .stTabs [aria-selected="true"] {
        background-color: #9c27b0 !important;
        color: #ffffff !important;
    }

    /* Cards and containers */
    .course-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(156,39,176,0.1);
        margin-bottom: 15px;
        border: 1px solid #9c27b0;
    }

    .highlight {
        background-color: #f3e5f5;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #9c27b0;
        color: #6a1b9a;
    }

    /* Buttons */
    .stButton > button {
        background-color: #9c27b0 !important;
        color: #ffffff !important;
        font-weight: bold !important;
        padding: 10px 20px !important;
        border-radius: 5px !important;
    }

    .stButton > button:hover {
        background-color: #7b1fa2 !important;
    }

    /* Skills tags */
    .skill-tag {
        background-color: #f3e5f5;
        color: #6a1b9a;
        padding: 5px 10px;
        border-radius: 15px;
        font-size: 14px;
        margin-right: 5px;
        display: inline-block;
        border: 1px solid #ce93d8;
    }

    /* Alerts and messages */
    .stAlert {
        background-color: #ffffff;
        color: #6a1b9a !important;
        border-radius: 5px;
        border: 1px solid #6a1b9a;
    }

    /* Links */
    a {
        color: #9c27b0 !important;
        text-decoration: none;
    }

    a:hover {
        text-decoration: underline;
    }

    /* Custom containers */
    .content-box {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        margin: 10px 0;
    }

    .info-box {
        background-color: #f3e5f5;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        border: 1px solid #ce93d8;
    }

    /* Text input placeholder color */
    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder {
        color: #e1bee7 !important;
    }

    /* Dark text elements */
    h1, h2, h3, h4, h5, h6 {
        color: #4a148c !important;
    }

    strong {
        color: #6a1b9a !important;
    }
</style>
""", unsafe_allow_html=True)

# Add this near the top of your app, after st.set_page_config
st.markdown("""
<style>
    .course-container {
        background-color: #f3e5f5;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        border: 1px solid #9c27b0;
    }
    .course-title {
        color: #4a148c;
        font-size: 1.5rem;
        font-weight: bold;
    }
    .course-metadata {
        color: #6a1b9a;
        font-size: 1rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Load more comprehensive course data
@st.cache_data
def load_course_data():
    # In a production environment, this would come from a database
    courses_data = {
        'course_id': range(1, 21),
        'title': [
            'Introduction to Python Programming',
            'Data Structures and Algorithms',
            'Web Development Fundamentals',
            'Machine Learning Basics',
            'Database Management Systems',
            'Software Engineering Principles',
            'Artificial Intelligence',
            'Cloud Computing',
            'Cybersecurity Fundamentals',
            'Mobile App Development',
            'Advanced Data Science',
            'DevOps Engineering',
            'Blockchain Development',
            'UI/UX Design Principles',
            'Natural Language Processing',
            'Computer Vision Fundamentals',
            'Quantum Computing Basics',
            'Internet of Things (IoT)',
            'Game Development Foundations',
            'Augmented Reality Applications'
        ],
        'description': [
            'Learn the fundamentals of Python programming language with hands-on exercises.',
            'Master essential data structures and algorithms for efficient problem-solving.',
            'Build responsive websites using HTML, CSS, and JavaScript.',
            'Introduction to machine learning concepts, algorithms, and applications.',
            'Design and manage relational databases with SQL.',
            'Learn software development lifecycle and best practices in engineering.',
            'Explore AI concepts, machine learning, and neural networks.',
            'Master cloud infrastructure, services, and deployment models.',
            'Learn essential cybersecurity concepts, threats, and defenses.',
            'Develop cross-platform mobile applications using modern frameworks.',
            'Advanced techniques in data manipulation, visualization, and predictive modeling.',
            'Implement continuous integration and deployment workflows.',
            'Learn blockchain technology and smart contract development.',
            'Master the principles of user experience and interface design.',
            'Build systems that can understand and process human language.',
            'Develop applications that can interpret and understand visual information.',
            'Introduction to quantum computing principles and algorithms.',
            'Connect and control devices in the Internet of Things ecosystem.',
            'Create interactive games using modern game engines.',
            'Develop applications that blend digital content with the real world.'
        ],
        'difficulty': [
            'Beginner', 'Intermediate', 'Beginner', 'Intermediate', 'Intermediate',
            'Intermediate', 'Advanced', 'Intermediate', 'Beginner', 'Intermediate',
            'Advanced', 'Advanced', 'Advanced', 'Intermediate', 'Advanced',
            'Advanced', 'Advanced', 'Intermediate', 'Intermediate', 'Advanced'
        ],
        'category': [
            'Programming', 'Computer Science', 'Web Development', 'Data Science',
            'Database', 'Software Engineering', 'AI/ML', 'Cloud', 'Security', 'Mobile Development',
            'Data Science', 'DevOps', 'Blockchain', 'Design', 'AI/ML',
            'AI/ML', 'Quantum Computing', 'IoT', 'Game Development', 'AR/VR'
        ],
        'duration_weeks': [
            4, 8, 6, 10, 6, 12, 14, 8, 5, 10,
            12, 8, 10, 6, 12, 10, 14, 8, 10, 12
        ],
        'skills_gained': [
            ['Python', 'Programming Fundamentals', 'Problem Solving'],
            ['Algorithms', 'Data Structures', 'Computational Thinking'],
            ['HTML', 'CSS', 'JavaScript', 'Responsive Design'],
            ['Machine Learning', 'Python', 'Data Analysis'],
            ['SQL', 'Database Design', 'Data Modeling'],
            ['Agile', 'Git', 'Testing', 'Project Management'],
            ['Neural Networks', 'Deep Learning', 'Python'],
            ['AWS', 'Azure', 'Virtualization', 'Containers'],
            ['Network Security', 'Encryption', 'Vulnerability Assessment'],
            ['iOS', 'Android', 'React Native', 'Flutter'],
            ['Advanced Statistics', 'BigData', 'Visualization', 'MLOps'],
            ['CI/CD', 'Docker', 'Kubernetes', 'Infrastructure as Code'],
            ['Smart Contracts', 'Ethereum', 'Solidity', 'Web3'],
            ['Wireframing', 'Prototyping', 'User Research', 'Usability Testing'],
            ['NLP', 'BERT', 'Transformers', 'Language Models'],
            ['OpenCV', 'CNNs', 'Image Processing', 'Object Detection'],
            ['Qubits', 'Quantum Gates', 'Quantum Algorithms'],
            ['Sensors', 'Embedded Systems', 'MQTT', 'Edge Computing'],
            ['Unity', 'Unreal Engine', '3D Modeling', 'Game Physics'],
            ['ARKit', 'ARCore', '3D Rendering', 'Spatial Computing']
        ],
        'prerequisites': [
            ['None'],
            ['Introduction to Programming'],
            ['Basic HTML/CSS Knowledge'],
            ['Python Programming', 'Basic Statistics'],
            ['Basic Computer Skills'],
            ['Programming Experience', 'Version Control'],
            ['Machine Learning Basics', 'Advanced Mathematics'],
            ['Networking Fundamentals', 'Basic Programming'],
            ['Basic Networking Knowledge'],
            ['Object-Oriented Programming'],
            ['Machine Learning Basics', 'Python Programming'],
            ['Linux Administration', 'Programming Experience'],
            ['Web Development', 'Cryptography Basics'],
            ['Graphic Design Basics'],
            ['Machine Learning', 'Python Programming'],
            ['Machine Learning', 'Linear Algebra'],
            ['Advanced Physics', 'Linear Algebra'],
            ['Basic Electronics', 'Programming Experience'],
            ['Programming Experience', '3D Graphics Basics'],
            ['Mobile Development', '3D Graphics']
        ],
        'rating': [
            4.7, 4.5, 4.8, 4.6, 4.3, 4.5, 4.9, 4.4, 4.7, 4.5,
            4.8, 4.6, 4.7, 4.5, 4.8, 4.9, 4.6, 4.3, 4.7, 4.8
        ],
        'career_relevance': [
            ['Software Developer', 'Data Analyst', 'QA Engineer'],
            ['Software Engineer', 'Backend Developer', 'Research Scientist'],
            ['Front-end Developer', 'Web Designer', 'UI Developer'],
            ['Data Scientist', 'Machine Learning Engineer', 'Research Analyst'],
            ['Database Administrator', 'Data Architect', 'Backend Developer'],
            ['Project Manager', 'Software Engineer', 'Product Manager'],
            ['AI Researcher', 'Machine Learning Engineer', 'Data Scientist'],
            ['Cloud Architect', 'DevOps Engineer', 'Solutions Architect'],
            ['Security Analyst', 'Penetration Tester', 'Security Engineer'],
            ['Mobile Developer', 'App Designer', 'UI/UX Developer'],
            ['Senior Data Scientist', 'AI Specialist', 'Research Scientist'],
            ['DevOps Engineer', 'Site Reliability Engineer', 'Cloud Architect'],
            ['Blockchain Developer', 'Smart Contract Engineer', 'Crypto Specialist'],
            ['UX Designer', 'Product Designer', 'UI Developer'],
            ['NLP Engineer', 'AI Researcher', 'Data Scientist'],
            ['Computer Vision Engineer', 'AI Researcher', 'Robotics Engineer'],
            ['Quantum Researcher', 'Quantum Software Engineer', 'Physicist'],
            ['IoT Engineer', 'Embedded Systems Developer', 'Solutions Architect'],
            ['Game Developer', 'Game Designer', '3D Modeler'],
            ['AR Developer', 'VR Engineer', 'Unity Developer']
        ]
    }
    return pd.DataFrame(courses_data)

# Load course data at startup
if 'courses_df' not in st.session_state:
    st.session_state.courses_df = load_course_data()

courses_df = st.session_state.courses_df

# User session management
def init_session_state():
    if 'user_id' not in st.session_state:
        st.session_state.user_id = str(uuid.uuid4())
    if 'history' not in st.session_state:
        st.session_state.history = []
    if 'profile' not in st.session_state:
        st.session_state.profile = {
            'interests': [],
            'learning_style': '',
            'career_goal': '',
            'completed_courses': []
        }
    if 'recommended_courses' not in st.session_state:
        st.session_state.recommended_courses = None

init_session_state()

def analyze_user_profile(interests, career_goal):
    """Analyze user interests and career goals to identify key learning priorities"""

    analysis_prompt = f"""
    Analyze this student's profile and identify key learning priorities:

    Interests: {interests}
    Career Goal: {career_goal}

    Provide analysis in JSON format:
    {{
        "core_skills_needed": ["list of 3-5 most important skills for the career goal"],
        "interest_areas": ["list of main interest domains"],
        "recommended_learning_path": ["ordered list of 3-4 learning areas from basic to advanced"],
        "career_alignment": "brief analysis of how interests align with career goal"
    }}
    """

    try:
        response = model.generate_content(analysis_prompt)
        return json.loads(response.text)
    except Exception as e:
        # Fallback analysis
        return {
            "core_skills_needed": ["programming", "data analysis", "problem solving"],
            "interest_areas": interests.split(','),
            "recommended_learning_path": ["fundamentals", "core technologies", "advanced concepts"],
            "career_alignment": f"Focus on building skills that bridge {interests} with {career_goal}"
        }

def calculate_course_relevance_score(course, interests, career_goal, profile_analysis):
    """Calculate a relevance score for a course based on user profile"""
    score = 0

    # Career relevance score (0-40 points)
    career_keywords = [goal.lower() for goal in career_goal.split()]
    career_match = sum(1 for keyword in career_keywords
                     if any(keyword in rel.lower() for rel in course['career_relevance']))
    score += (career_match / len(career_keywords)) * 40 if career_keywords else 0

    # Interest alignment score (0-30 points)
    interest_keywords = [int.lower() for int in interests.split(',')]
    interest_match = sum(1 for keyword in interest_keywords
                       if keyword in course['description'].lower())
    score += (interest_match / len(interest_keywords)) * 30 if interest_keywords else 0

    # Core skills coverage score (0-20 points)
    skills_match = sum(1 for skill in profile_analysis['core_skills_needed']
                     if any(skill.lower() in s.lower() for s in course['skills_gained']))
    score += (skills_match / len(profile_analysis['core_skills_needed'])) * 20

    # Learning path alignment score (0-10 points)
    try:
        path_position = profile_analysis['recommended_learning_path'].index(course['difficulty'].lower())
        score += (1 - (path_position / len(profile_analysis['recommended_learning_path']))) * 10
    except ValueError:
        # If the difficulty level is not in the recommended path, add no points
        pass

    return score

def get_personalized_recommendations(interests, learning_style, career_goal, experience_level='Beginner'):
    """Generate highly personalized course recommendations based on detailed profile analysis"""

    # First, analyze the user's profile
    profile_analysis = analyze_user_profile(interests, career_goal)

    # Enhanced recommendation prompt with analysis insights
    prompt = f"""
    Based on detailed student profile analysis:

    STUDENT PROFILE:
    - Interests: {interests}
    - Career Goal: {career_goal}
    - Experience Level: {experience_level}
    - Learning Style: {learning_style}

    ANALYSIS INSIGHTS:
    - Core Skills Needed: {', '.join(profile_analysis['core_skills_needed'])}
    - Interest Areas: {', '.join(profile_analysis['interest_areas'])}
    - Recommended Path: {' → '.join(profile_analysis['recommended_learning_path'])}
    - Career Alignment: {profile_analysis['career_alignment']}

    Recommend courses that:
    1. Build the identified core skills
    2. Follow the recommended learning path
    3. Match the student's interests
    4. Support the career goal
    5. Consider learning style preferences

    Available courses:
    {courses_df[['course_id', 'title', 'description', 'difficulty', 'category', 'skills_gained', 'career_relevance']].to_string()}

    Return ONLY a comma-separated list of course IDs, ordered by relevance.
    """

    try:
        # Get AI recommendations
        response = model.generate_content(prompt)
        ai_recommended_courses = [
            int(item) for item in response.text.strip().replace(',', ' ').split()
            if item.isdigit() and int(item) in courses_df['course_id'].values
        ]

        # Score and sort courses
        course_scores = []
        for course_id in ai_recommended_courses:
            course = courses_df[courses_df['course_id'] == course_id].iloc[0]
            relevance_score = calculate_course_relevance_score(
                course,
                interests,
                career_goal,
                profile_analysis
            )
            course_scores.append((course_id, relevance_score))

        # Sort by score and get course IDs
        sorted_courses = [course_id for course_id, _ in
                        sorted(course_scores, key=lambda x: x[1], reverse=True)]

        # Apply difficulty and prerequisite filtering
        final_recommendations = filter_and_sequence_courses(
            sorted_courses, experience_level, courses_df)

        return final_recommendations[:8]

    except Exception as e:
        st.error(f"Error in recommendation generation: {str(e)}")
        return fallback_recommendations(career_goal, courses_df)

def filter_and_sequence_courses(course_ids, experience_level, courses_df):
    """Filter and sequence courses based on difficulty and prerequisites"""
    difficulty_order = ['Beginner', 'Intermediate', 'Advanced']
    current_level_index = difficulty_order.index(experience_level)

    filtered_courses = []
    prerequisites_map = {}

    # Build prerequisites map
    for course_id in course_ids:
        course = courses_df[courses_df['course_id'] == course_id].iloc[0]
        prerequisites_map[course_id] = set(course['prerequisites'])

    # Filter and sequence courses
    for course_id in course_ids:
        course = courses_df[courses_df['course_id'] == course_id].iloc[0]
        course_difficulty_index = difficulty_order.index(course['difficulty'])

        # Check difficulty level appropriateness
        if course_difficulty_index <= current_level_index + 1:
            # Add prerequisites first
            prereqs = prerequisites_map[course_id]
            for prereq in prereqs:
                prereq_courses = courses_df[
                    courses_df['skills_gained'].apply(lambda x: prereq in x)
                ]
                if not prereq_courses.empty:
                    filtered_courses.extend(prereq_courses['course_id'].tolist())

            filtered_courses.append(course_id)

    # Remove duplicates while preserving order
    return list(dict.fromkeys(filtered_courses))

def fallback_recommendations(career_goal, courses_df):
    """Provide fallback recommendations based on career goal"""
    career_matches = courses_df[
        courses_df['career_relevance'].apply(
            lambda x: any(goal.lower() in career_goal.lower() for goal in x)
        )
    ]
    return career_matches.sort_values('rating', ascending=False)['course_id'].tolist()[:8]

# Function to get detailed explanation for why a course was recommended
def get_course_explanation(course, interests, learning_style, career_goal):
    """Generate personalized explanation for why a course was recommended"""
    prompt = f"""
    Explain in 2-3 sentences why the course "{course['title']}" is specifically recommended for this student:

    Student Profile:
    - Interests: {interests}
    - Learning Style: {learning_style}
    - Career Goal: {career_goal}

    Course Details:
    - Category: {course['category']}
    - Difficulty: {course['difficulty']}
    - Skills: {', '.join(course['skills_gained'])}
    - Career Relevance: {', '.join(course['career_relevance'])}

    Focus on:
    1. How it aligns with their career goal
    2. Why it matches their interests
    3. How it fits their learning style

    Keep the explanation personal and specific to their profile.
    """

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        # Fallback explanation
        return f"This {course['difficulty']} level course in {course['category']} aligns with your interest in {interests.split(',')[0]} and provides essential skills for {career_goal}. The course's format is well-suited for {learning_style} learners."

# Function to generate a learning path visualization
def generate_learning_path_visualization(recommended_course_ids):
    if not recommended_course_ids:
        return None

    courses = [courses_df[courses_df['course_id'] == id].iloc[0] for id in recommended_course_ids]

    # Prepare data for visualization
    timeline_data = []
    current_week = 0

    for i, course in enumerate(courses):
        start_week = current_week
        end_week = current_week + course['duration_weeks']

        timeline_data.append({
            'Course': course['title'],
            'Category': course['category'],
            'Start': start_week,
            'End': end_week,
            'Difficulty': course['difficulty'],
            'Order': i + 1
        })

        # Add a small gap between courses
        current_week = end_week + 1

    timeline_df = pd.DataFrame(timeline_data)

    # Create the Altair chart
    chart = alt.Chart(timeline_df).mark_bar().encode(
        x=alt.X('Start:Q', title='Week'),
        x2=alt.X2('End:Q'),
        y=alt.Y('Course:N', sort=alt.EncodingSortField(field='Order', order='descending'), title=None),
        color=alt.Color('Category:N', legend=alt.Legend(title="Course Category")),
        tooltip=['Course', 'Category', 'Difficulty', 'Start', 'End']
    ).properties(
        title='Your Learning Path Timeline',
        width=700,
        height=300
    ).configure_axisY(
        labelLimit=200
    )

    return chart

# Function to generate a skill development chart
def generate_skill_chart(recommended_course_ids):
    # Extract and count skills from recommended courses
    skills = []
    for course_id in recommended_course_ids:
        # Get the course details from courses_df
        course = courses_df[courses_df['course_id'] == course_id].iloc[0]
        skills.extend(course['skills_gained'])

    skill_counts = pd.DataFrame({
        'Skill': skills
    }).value_counts().reset_index()
    skill_counts.columns = ['Skill', 'Count']

    # Create the chart with a valid color scheme
    skill_chart = alt.Chart(skill_counts).mark_bar().encode(
        y=alt.Y('Skill:N', sort='-x', title=None),
        x=alt.X('Count:Q', title='Number of Courses'),
        color=alt.Color('Count:Q',
                       legend=None,
                       scale=alt.Scale(scheme='blues')),
        tooltip=['Skill', 'Count']
    ).properties(
        title='Skills Coverage in Recommended Courses',
        width=600,
        height=alt.Step(30)  # Adjust bar height
    )

    return skill_chart

# Function to get AI-recommended additional learning resources for a course
def get_additional_resources(course_title, skills):
    """Get AI-recommended additional learning resources for a course with specific YouTube recommendations"""
    prompt = f"""
    As a technical education expert, recommend specific YouTube tutorials for the course "{course_title}"
    that teaches {', '.join(skills)}.

    Provide 4 highly-specific YouTube video recommendations in these categories:
    1. One comprehensive course overview
    2. One beginner-friendly tutorial
    3. One practical project-based tutorial
    4. One advanced concepts deep-dive

    Format as JSON with this structure:
    {{
        "youtube_recommendations": [
            {{
                "title": "exact video title",
                "creator": "channel name",
                "duration": "approximate duration (e.g. '2 hours', '45 minutes')",
                "level": "beginner/intermediate/advanced",
                "search_query": "optimized search query",
                "description": "brief description of what this video covers"
            }}
        ]
    }}

    Make recommendations extremely specific and realistic.
    """

    try:
        response = model.generate_content(prompt)
        recommendations = json.loads(response.text)

        # Update the display_course_recommendation function to show the enhanced recommendations
        return recommendations
    except Exception as e:
        # Fallback recommendations with more structure
        return {
            "youtube_recommendations": [
                {
                    "title": f"Complete {course_title} Course 2024",
                    "creator": "Tech Education",
                    "duration": "8 hours",
                    "level": "beginner",
                    "search_query": f"{course_title} complete course tutorial",
                    "description": "Comprehensive course covering all fundamentals"
                },
                {
                    "title": f"{course_title} for Absolute Beginners",
                    "creator": "Programming Made Simple",
                    "duration": "2 hours",
                    "level": "beginner",
                    "search_query": f"{course_title} beginners tutorial",
                    "description": "Step-by-step introduction to core concepts"
                },
                {
                    "title": f"Build a Real-World Project with {course_title}",
                    "creator": "Coding Projects",
                    "duration": "3 hours",
                    "level": "intermediate",
                    "search_query": f"{course_title} project tutorial",
                    "description": "Hands-on project implementation"
                },
                {
                    "title": f"Advanced {course_title} Concepts Explained",
                    "creator": "Tech Deep Dives",
                    "duration": "1.5 hours",
                    "level": "advanced",
                    "search_query": f"advanced {course_title} tutorial",
                    "description": "In-depth coverage of advanced topics"
                }
            ]
        }

def display_course_recommendation(course, explanation, index):
    """Display a course recommendation with enhanced styling"""
    with st.container():
        # Create a visually distinct course card
        st.markdown("""
        <style>
        .course-card {
            background-color: #f3e5f5;
            padding: 20px;
            border-radius: 10px;
            border: 2px solid #9c27b0;
            margin-bottom: 20px;
        }
        .course-number {
            background-color: #9c27b0;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            display: inline-block;
            margin-right: 10px;
            font-weight: bold;
        }
        </style>
        """, unsafe_allow_html=True)

        # Course number and title
        st.markdown(f"""
        <div class="course-card">
            <div>
                <span class="course-number">{index + 1}</span>
                <span style="font-size: 24px; font-weight: bold; color: #4a148c;">{course['title']}</span>
            </div>
        """, unsafe_allow_html=True)

        # Course metadata (removed rating)
        st.markdown(f"**Difficulty:** {course['difficulty']} | **Category:** {course['category']} | **Duration:** {course['duration_weeks']} weeks")

        # Course description
        st.markdown("### Description")
        st.write(course['description'])

        # Why this course section
        st.markdown("### Why this course?")
        st.write(explanation)

        # Skills and Prerequisites in columns
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### Skills you'll gain")
            skills_list = "".join([f"- {skill}\n" for skill in course['skills_gained']])
            st.markdown(skills_list)

        with col2:
            st.markdown("### Prerequisites")
            prereq_list = "".join([f"- {prereq}\n" for prereq in course['prerequisites']])
            st.markdown(prereq_list)

        # Career Relevance
        st.markdown("### Career Relevance")
        careers_list = "".join([f"- {career}\n" for career in course['career_relevance']])
        st.markdown(careers_list)

        # Additional Resources - Enhanced YouTube recommendations
        with st.expander("📺 Recommended Video Tutorials"):
            resources = get_additional_resources(course['title'], course['skills_gained'])

            for video in resources['youtube_recommendations']:
                st.markdown(f"""
                ### {video['title']}
                - 👤 **Creator:** {video['creator']}
                - ⏱️ **Duration:** {video['duration']}
                - 📊 **Level:** {video['level'].capitalize()}
                - 📝 **Description:** {video['description']}
                - 🔗 [Watch on YouTube](https://www.youtube.com/results?search_query={video['search_query'].replace(' ', '+')})
                ---
                """)

        # Close the course card div
        st.markdown("</div>", unsafe_allow_html=True)

# Main application
def generate_daily_timetable(recommended_courses, learning_style):
    """Generate a personalized daily study timetable based on recommended courses and learning style"""

    # Define learning activities for each style
    learning_activities = {
        'Visual': [
            'Watch video tutorials',
            'Study diagrams and flowcharts',
            'Create mind maps',
            'Review visual documentation'
        ],
        'Auditory': [
            'Listen to lectures',
            'Participate in discussion groups',
            'Record and review notes',
            'Explain concepts aloud'
        ],
        'Reading/Writing': [
            'Read documentation',
            'Take detailed notes',
            'Write code summaries',
            'Review written materials'
        ],
        'Kinesthetic': [
            'Complete hands-on exercises',
            'Build practice projects',
            'Debug sample code',
            'Implement concepts practically'
        ]
    }

    # Initialize weekly schedule
    weekly_schedule = {
        'Monday': {},
        'Tuesday': {},
        'Wednesday': {},
        'Thursday': {},
        'Friday': {},
        'Saturday': {},
        'Sunday': {'rest_day': True}
    }

    # Define time slots based on learning style and difficulty
    time_slots = {
        'Visual': {
            'Beginner': ['19:00 - 20:30'],
            'Intermediate': ['18:00 - 20:00'],
            'Advanced': ['17:00 - 20:00']
        },
        'Auditory': {
            'Beginner': ['10:00 - 11:30'],
            'Intermediate': ['10:00 - 12:00'],
            'Advanced': ['09:00 - 12:00']
        },
        'Reading/Writing': {
            'Beginner': ['15:00 - 16:30'],
            'Intermediate': ['14:00 - 16:00'],
            'Advanced': ['14:00 - 17:00']
        },
        'Kinesthetic': {
            'Beginner': ['16:00 - 17:30'],
            'Intermediate': ['16:00 - 18:00'],
            'Advanced': ['15:00 - 18:00']
        }
    }

    # Distribute courses across the week
    current_course_index = 0
    for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']:
        if current_course_index >= len(recommended_courses):
            current_course_index = 0

        course = recommended_courses[current_course_index]

        # Get appropriate time slots based on learning style and difficulty
        style_slots = time_slots.get(learning_style, time_slots['Visual'])
        course_slots = style_slots.get(course['difficulty'], style_slots['Beginner'])

        # Get appropriate activities based on learning style
        activities = learning_activities.get(learning_style, learning_activities['Visual'])

        weekly_schedule[day] = {
            'course': course['title'],
            'difficulty': course['difficulty'],
            'time_slots': course_slots,
            'activities': activities
        }
        current_course_index += 1

    return weekly_schedule

def display_timetable(weekly_schedule):
    """Display the generated timetable in a structured format"""

    # Create tabs for each day
    days = list(weekly_schedule.keys())
    day_tabs = st.tabs(days)

    for day, tab in zip(days, day_tabs):
        with tab:
            if day == 'Sunday':
                st.markdown("### 🌟 Rest and Review Day")
                st.markdown("""
                - Review the week's progress
                - Organize study materials
                - Plan for next week
                - Take time to rest and recharge
                """)
            else:
                schedule = weekly_schedule[day]

                # Create columns for better layout
                col1, col2 = st.columns([1, 1])

                with col1:
                    st.markdown(f"### 📚 {schedule['course']}")
                    st.markdown(f"**Difficulty Level:** {schedule['difficulty']}")

                    st.markdown("### ⏰ Study Sessions:")
                    for time_slot in schedule['time_slots']:
                        st.markdown(f"- {time_slot}")

                with col2:
                    st.markdown("### 📝 Learning Activities:")
                    for activity in schedule['activities']:
                        st.markdown(f"- {activity}")

def generate_pdf(recommended_courses, weekly_schedule, profile):
    """Generate a PDF with course recommendations and timetable"""
    try:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            pdf_path = tmp_file.name

        # Create the PDF document with margins
        doc = SimpleDocTemplate(
            pdf_path,
            pagesize=letter,
            leftMargin=0.75*inch,
            rightMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )
        styles = getSampleStyleSheet()
        elements = []

        # Create a custom title style
        title_style = ParagraphStyle(
            'Title',
            parent=styles['Heading1'],
            fontSize=22,
            textColor=colors.Color(0.4, 0.1, 0.5),  # Dark purple
            alignment=1,  # Center alignment
            spaceAfter=6,
            leading=26
        )

        # Create a custom subtitle style
        subtitle_style = ParagraphStyle(
            'Subtitle',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.Color(0.5, 0.3, 0.6),  # Medium purple
            alignment=1,  # Center alignment
            spaceAfter=20,
            leading=18
        )

        # Add title and subtitle
        elements.append(Paragraph("Your Personalized Learning Path", title_style))
        elements.append(Paragraph("EduPathfinder - Building Your Educational Journey", subtitle_style))

        # Add a horizontal line using a table instead of HorizontalLine
        elements.append(Spacer(1, 0.1*inch))

        # Create a simple table as a horizontal line
        hr_color = colors.Color(0.8, 0.7, 0.9)  # Light purple
        hr = Table([['']],
                  colWidths=[7*inch],
                  rowHeights=[0.5])
        hr.setStyle(TableStyle([
            ('LINEBELOW', (0, 0), (-1, -1), 2, hr_color),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        elements.append(hr)

        elements.append(Spacer(1, 0.25*inch))

        # Add profile information
        profile_style = ParagraphStyle(
            'Profile',
            parent=styles['Normal'],
            fontSize=12,
            spaceAfter=6
        )
        elements.append(Paragraph(f"<b>Name:</b> {profile.get('name', 'Student')}", profile_style))
        elements.append(Paragraph(f"<b>Interests:</b> {profile.get('interests', '')}", profile_style))
        elements.append(Paragraph(f"<b>Learning Style:</b> {profile.get('learning_style', '')}", profile_style))
        elements.append(Paragraph(f"<b>Career Goal:</b> {profile.get('career_goal', '')}", profile_style))
        elements.append(Paragraph(f"<b>Experience Level:</b> {profile.get('experience_level', '')}", profile_style))
        elements.append(Spacer(1, 0.25*inch))

        # Add recommended courses section with better formatting
        elements.append(Paragraph("Recommended Courses", styles['Heading2']))
        elements.append(Spacer(1, 0.1*inch))

        # Create a custom style for course titles
        course_title_style = ParagraphStyle(
            'CourseTitle',
            parent=styles['Heading3'],
            fontSize=14,
            textColor=colors.Color(0.4, 0.1, 0.5),  # Dark purple
            spaceAfter=6,
            spaceBefore=12,
            borderWidth=1,
            borderColor=colors.Color(0.8, 0.7, 0.9),  # Light purple
            borderPadding=8,
            borderRadius=5,
            leading=16
        )

        # Create a custom style for course details
        course_detail_style = ParagraphStyle(
            'CourseDetail',
            parent=styles['Normal'],
            fontSize=11,
            spaceAfter=4,
            leftIndent=20,
            leading=14
        )

        # Create a custom style for section headers within courses
        section_header_style = ParagraphStyle(
            'SectionHeader',
            parent=styles['Normal'],
            fontSize=11,
            fontName='Helvetica-Bold',
            textColor=colors.Color(0.3, 0.3, 0.5),  # Dark blue-purple
            spaceBefore=8,
            spaceAfter=4,
            leftIndent=20,
            leading=14
        )

        # Create a custom style for skills list
        skill_style = ParagraphStyle(
            'Skill',
            parent=styles['Normal'],
            fontSize=10,
            leftIndent=40,
            firstLineIndent=-15,  # For bullet points
            leading=14
        )

        # Add each course with improved formatting
        for i, course in enumerate(recommended_courses, 1):
            # Course title with number and difficulty level
            elements.append(Paragraph(
                f"{i}. {course['title']} <i>({course['difficulty']})</i>",
                course_title_style
            ))

            # Course details in a more organized format
            elements.append(Paragraph(
                f"<b>Category:</b> {course['category']} | <b>Duration:</b> {course['duration_weeks']} weeks",
                course_detail_style
            ))

            # Description if available
            if 'description' in course:
                elements.append(Paragraph(
                    f"<i>{course['description']}</i>",
                    course_detail_style
                ))

            # Skills section
            elements.append(Paragraph("Skills you'll gain:", section_header_style))

            # Add skills as bullet points
            for skill in course['skills_gained']:
                elements.append(Paragraph(f"• {skill}", skill_style))

            # Career relevance if available
            if 'career_relevance' in course:
                elements.append(Paragraph("Career Relevance:", section_header_style))
                careers_text = ", ".join(course['career_relevance'][:3])
                if len(course['career_relevance']) > 3:
                    careers_text += ", and more"
                elements.append(Paragraph(careers_text, course_detail_style))

            # Add a separator between courses
            if i < len(recommended_courses):
                elements.append(Spacer(1, 0.2*inch))

        # Add weekly timetable section
        elements.append(Paragraph("Weekly Study Schedule", styles['Heading2']))
        elements.append(Spacer(1, 0.1*inch))

        # Create timetable data with better formatting
        timetable_data = [["Day", "Course", "Time Slots", "Learning Activities"]]

        # Define day order to ensure consistent presentation
        day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

        for day in day_order:
            if day == "Sunday":
                timetable_data.append([
                    day,
                    "Rest Day",
                    "N/A",
                    "• Review the week's progress\n• Organize study materials\n• Plan for next week\n• Rest and recharge"
                ])
            else:
                schedule = weekly_schedule[day]

                # Format time slots with bullet points
                time_slots_formatted = "\n".join([f"• {slot}" for slot in schedule['time_slots']])

                # Format activities with bullet points (limit to 3)
                activities_formatted = "\n".join([f"• {activity}" for activity in schedule['activities'][:3]])
                if len(schedule['activities']) > 3:
                    activities_formatted += "\n• ..."

                timetable_data.append([
                    day,
                    schedule['course'] + "\n(" + schedule['difficulty'] + ")",
                    time_slots_formatted,
                    activities_formatted
                ])

        # Create the table with adjusted column widths
        table = Table(timetable_data, colWidths=[0.8*inch, 1.8*inch, 1.4*inch, 3.0*inch], repeatRows=1)

        # Add style to the table for better readability
        purple_color = colors.Color(0.6, 0.1, 0.6)  # Darker purple
        light_purple = colors.Color(0.95, 0.9, 0.95)  # Very light purple
        alternate_color = colors.Color(0.9, 0.85, 0.9)  # Slightly darker for alternating rows

        table_style = TableStyle([
            # Header row styling
            ('BACKGROUND', (0, 0), (-1, 0), purple_color),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),

            # Alternating row colors for better readability
            ('BACKGROUND', (0, 1), (-1, -1), light_purple),
            ('BACKGROUND', (0, 2), (-1, 2), alternate_color),
            ('BACKGROUND', (0, 4), (-1, 4), alternate_color),
            ('BACKGROUND', (0, 6), (-1, 6), alternate_color),

            # Grid styling
            ('GRID', (0, 0), (-1, -1), 1, colors.darkgrey),
            ('BOX', (0, 0), (-1, -1), 2, colors.black),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.black),

            # Text alignment
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (0, 0), (0, -1), 'CENTER'),  # Center day column
            ('ALIGN', (1, 1), (1, -1), 'LEFT'),    # Left align course column
            ('ALIGN', (2, 1), (2, -1), 'LEFT'),    # Left align time slots
            ('ALIGN', (3, 1), (3, -1), 'LEFT'),    # Left align activities

            # Font settings
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),

            # Padding
            ('TOPPADDING', (0, 1), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 12),
            ('LEFTPADDING', (0, 1), (-1, -1), 8),
            ('RIGHTPADDING', (0, 1), (-1, -1), 8),

            # Day column styling
            ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
            ('TEXTCOLOR', (0, 1), (0, -1), purple_color),

            # Sunday row styling (rest day)
            ('BACKGROUND', (0, 7), (-1, 7), colors.Color(0.9, 0.9, 0.95)),  # Light blue-ish for Sunday
            ('TEXTCOLOR', (1, 7), (1, 7), colors.darkblue),  # Dark blue for "Rest Day" text
        ])
        table.setStyle(table_style)

        elements.append(table)
        elements.append(Spacer(1, 0.25*inch))

        # Add a horizontal line before footer
        elements.append(Spacer(1, 0.25*inch))
        hr = Table([['']],
                  colWidths=[7*inch],
                  rowHeights=[0.5])
        hr.setStyle(TableStyle([
            ('LINEBELOW', (0, 0), (-1, -1), 1, colors.Color(0.8, 0.7, 0.9)),  # Light purple
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        elements.append(hr)
        elements.append(Spacer(1, 0.1*inch))

        # Add footer with more information
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.Color(0.5, 0.5, 0.5),  # Medium grey
            alignment=1,  # Center alignment
            leading=12
        )

        # Get current date
        from datetime import datetime
        current_date = datetime.now().strftime("%B %d, %Y")

        # Add footer text
        elements.append(Paragraph(
            f"Generated by EduPathfinder on {current_date}",
            footer_style
        ))
        elements.append(Paragraph(
            "Your Personalized Learning Journey",
            footer_style
        ))

        # Add copyright notice
        copyright_style = ParagraphStyle(
            'Copyright',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.Color(0.6, 0.6, 0.6),  # Light grey
            alignment=1,  # Center alignment
            leading=10
        )
        elements.append(Spacer(1, 0.05*inch))
        elements.append(Paragraph(
            f"© {datetime.now().year} EduPathfinder. All rights reserved.",
            copyright_style
        ))

        # Build the PDF with a simpler approach
        # Add page numbers as a footer on each page
        def add_page_number(canvas, doc):
            canvas.saveState()
            canvas.setFont('Helvetica', 8)
            canvas.setFillColor(colors.Color(0.5, 0.5, 0.5))  # Medium grey
            page_num = canvas.getPageNumber()
            text = f"Page {page_num}"
            canvas.drawRightString(7.25*inch, 0.5*inch, text)
            canvas.restoreState()

        # Build the PDF with the page number function
        doc.build(elements, onFirstPage=add_page_number, onLaterPages=add_page_number)

        return pdf_path
    except Exception as e:
        st.error(f"Error generating PDF: {str(e)}")
        return None

def main():
    # Header with improved visibility
    st.markdown('<div class="content-box">', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 5])
    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/2436/2436874.png", width=80)
    with col2:
        st.markdown('<h1 style="margin-bottom: 0;">EduPathfinder</h1>', unsafe_allow_html=True)
        st.markdown('<p style="font-size: 18px; color: #666;">Building personalized learning journeys for your career success</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Navigation tabs
    tabs = st.tabs([
        "📋 Profile",
        "🎯 Recommendations",
        "📊 Learning Analytics",
        "ℹ️ About"
    ])

    with tabs[0]:  # Profile Tab
        st.markdown('<div class="content-box">', unsafe_allow_html=True)
        st.markdown('<h2>Your Learning Profile</h2>', unsafe_allow_html=True)

        col1, col2 = st.columns([2, 1])

        with col1:
            with st.form("profile_form"):
                st.markdown('<div class="info-box">', unsafe_allow_html=True)
                st.markdown('<h3>Personal Information</h3>', unsafe_allow_html=True)

                name = st.text_input(
                    "Name (Optional)",
                    help="Enter your name to personalize your experience"
                )
                st.markdown('</div>', unsafe_allow_html=True)

                st.markdown('<div class="info-box" style="margin-top: 20px;">', unsafe_allow_html=True)
                st.markdown('<h3>Learning Preferences</h3>', unsafe_allow_html=True)

                interests = st.text_area(
                    "What are your interests and topics you'd like to learn about?",
                    placeholder="e.g., Machine Learning, Web Development, Cybersecurity...",
                    help="List your technical interests, separated by commas"
                )

                learning_style = st.selectbox(
                    "What's your preferred learning style?",
                    list(learning_styles_characteristics.keys()),
                    help="Choose the learning style that best matches how you prefer to learn"
                )

                career_goal = st.text_area(
                    "What are your career goals or target roles?",
                    placeholder="e.g., Data Scientist, Software Engineer, Cloud Architect...",
                    help="Describe your target job roles or career aspirations"
                )

                experience_level = st.select_slider(
                    "Your current experience level",
                    options=["Beginner", "Intermediate", "Advanced"],
                    help="Select your current level of experience in your field of interest"
                )

                st.markdown('</div>', unsafe_allow_html=True)

                submit = st.form_submit_button("Save Profile")

                if submit:
                    if not interests or not career_goal:
                        st.error("Please fill in your interests and career goals.")
                    else:
                        st.session_state.profile.update({
                            'name': name,
                            'interests': interests,
                            'learning_style': learning_style,
                            'career_goal': career_goal,
                            'experience_level': experience_level
                        })
                        st.success("Profile saved successfully! Go to the Recommendations tab to see your personalized learning path.")

        with col2:
            if learning_style:
                st.markdown('<div class="info-box">', unsafe_allow_html=True)
                st.markdown(f'<h3>{learning_style} Learner</h3>', unsafe_allow_html=True)
                st.markdown(f'<p>{learning_styles_characteristics[learning_style]["description"]}</p>', unsafe_allow_html=True)

                st.markdown('<h4>Preferred Learning Methods</h4>', unsafe_allow_html=True)
                for method in learning_styles_characteristics[learning_style]["preferred_methods"]:
                    st.markdown(f'<div class="content-box" style="margin: 5px 0;">{method}</div>', unsafe_allow_html=True)

                st.markdown('<h4>Study Tips</h4>', unsafe_allow_html=True)
                for tip in learning_styles_characteristics[learning_style]["study_tips"]:
                    st.markdown(f'<div class="content-box" style="margin: 5px 0;">{tip}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    with tabs[1]:  # Recommendations Tab
        st.header("Your Personalized Learning Path")

        if not st.session_state.profile.get('interests') or not st.session_state.profile.get('career_goal'):
            st.info("Please complete your profile in the Profile tab to get personalized recommendations.")
        else:
            if st.button("Generate Recommendations"):
                with st.spinner("Analyzing your profile and generating personalized recommendations..."):
                    recommended_course_ids = get_personalized_recommendations(
                        st.session_state.profile.get('interests', ''),
                        st.session_state.profile.get('learning_style', ''),
                        st.session_state.profile.get('career_goal', ''),
                        st.session_state.profile.get('experience_level', 'Beginner')
                    )
                    st.session_state.recommended_courses = recommended_course_ids

            if st.session_state.recommended_courses:
                try:
                    # Get full course details
                    recommended_courses = []
                    for course_id in st.session_state.recommended_courses:
                        course_data = courses_df[courses_df['course_id'] == course_id]
                        if not course_data.empty:
                            recommended_courses.append(course_data.iloc[0].to_dict())

                    # Display recommendations
                    st.subheader("📚 Recommended Courses")
                    for i, course in enumerate(recommended_courses, 1):
                        explanation = get_course_explanation(
                            course,
                            st.session_state.profile.get('interests', ''),
                            st.session_state.profile.get('learning_style', ''),
                            st.session_state.profile.get('career_goal', '')
                        )
                        display_course_recommendation(course, explanation, i)

                    # Generate and display timetable
                    st.markdown("---")
                    st.header("📊 Weekly Study Schedule")

                    try:
                        weekly_schedule = generate_daily_timetable(
                            recommended_courses,
                            st.session_state.profile.get('learning_style', 'Visual')  # Default to Visual if not set
                        )
                        display_timetable(weekly_schedule)

                        # Add export buttons
                        col1, col2 = st.columns(2)

                        with col1:
                            # Export timetable as markdown
                            if st.button("📥 Export Timetable (Markdown)"):
                                markdown_content = "# Your Personal Study Timetable\n\n"
                                for day, schedule in weekly_schedule.items():
                                    markdown_content += f"## {day}\n"
                                    if day == 'Sunday':
                                        markdown_content += "- Rest and Review Day\n"
                                    else:
                                        markdown_content += f"### Course: {schedule['course']}\n"
                                        markdown_content += f"**Difficulty Level:** {schedule['difficulty']}\n\n"
                                        markdown_content += "#### Study Sessions:\n"
                                        for time_slot in schedule['time_slots']:
                                            markdown_content += f"- {time_slot}\n"
                                        markdown_content += "\n#### Learning Activities:\n"
                                        for activity in schedule['activities']:
                                            markdown_content += f"- {activity}\n"
                                    markdown_content += "\n---\n"

                                st.download_button(
                                    label="Download Timetable",
                                    data=markdown_content,
                                    file_name="study_timetable.md",
                                    mime="text/markdown"
                                )

                        with col2:
                            # Export complete learning path as PDF
                            if st.button("📥 Export Complete Learning Path (PDF)"):
                                with st.spinner("Generating PDF..."):
                                    try:
                                        # Install reportlab if not already installed
                                        try:
                                            import reportlab
                                        except ImportError:
                                            st.info("Installing required packages...")
                                            import subprocess
                                            subprocess.check_call(["pip", "install", "reportlab"])
                                            st.experimental_rerun()

                                        # Generate PDF
                                        pdf_path = generate_pdf(
                                            recommended_courses,
                                            weekly_schedule,
                                            st.session_state.profile
                                        )

                                        if pdf_path:
                                            # Read the PDF file
                                            with open(pdf_path, "rb") as pdf_file:
                                                pdf_bytes = pdf_file.read()

                                            # Offer download
                                            st.download_button(
                                                label="Download PDF",
                                                data=pdf_bytes,
                                                file_name="learning_path.pdf",
                                                mime="application/pdf"
                                            )

                                            # Clean up the temporary file
                                            import os
                                            os.unlink(pdf_path)
                                    except Exception as e:
                                        st.error(f"Error generating PDF: {str(e)}")
                                        st.info("Please make sure you have reportlab installed: pip install reportlab")
                    except Exception as e:
                        st.error(f"Error generating timetable: {str(e)}")
                        st.info("Please try again or contact support if the issue persists.")

                except Exception as e:
                    st.error(f"An error occurred while displaying recommendations: {str(e)}")

                # Removed the "Your Personalized Study Timetable" section to fix the error

                # Study Timeline section removed as requested

    with tabs[2]:  # Learning Analytics Tab
        st.header("Learning Analytics")

        if not st.session_state.recommended_courses:
            st.info("Generate recommendations first to see your learning analytics.")
        else:
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Curriculum Breakdown")

                # Get category distribution
                recommended_courses = [courses_df[courses_df['course_id'] == id].iloc[0] for id in st.session_state.recommended_courses]
                categories = [course['category'] for course in recommended_courses]
                category_counts = pd.Series(categories).value_counts().reset_index()
                category_counts.columns = ['Category', 'Count']

                # Create pie chart
                fig, ax = plt.subplots(figsize=(5, 5))
                ax.pie(category_counts['Count'], labels=category_counts['Category'], autopct='%1.1f%%',
                       startangle=90, shadow=False)
                ax.axis('equal')
                st.pyplot(fig)

            with col2:
                st.subheader("Difficulty Progression")

                # Map difficulty levels to numeric values
                difficulty_map = {'Beginner': 1, 'Intermediate': 2, 'Advanced': 3}

                # Create difficulty progression data
                difficulty_data = pd.DataFrame({
                    'Course': [course['title'] for course in recommended_courses],
                    'Difficulty': [difficulty_map[course['difficulty']] for course in recommended_courses],
                    'Order': range(1, len(recommended_courses) + 1)
                })

                # Create line chart
                difficulty_chart = alt.Chart(difficulty_data).mark_line(point=True).encode(
                    x=alt.X('Order:O', title='Course Order'),
                    y=alt.Y('Difficulty:Q', title='Difficulty Level', scale=alt.Scale(domain=[0.5, 3.5])),
                    tooltip=['Course', 'Order']
                ).properties(
                    title='Learning Path Difficulty Progression',
                    width=350,
                    height=250
                )

                st.altair_chart(difficulty_chart, use_container_width=True)

                # Add legend for difficulty levels
                st.markdown("""
                **Difficulty Scale:**
                - 1: Beginner
                - 2: Intermediate
                - 3: Advanced
                """)

            # Estimated completion time
            total_weeks = sum(course['duration_weeks'] for course in recommended_courses)
            st.markdown(f"### ⏱️ Estimated Completion Time: **{total_weeks} weeks**")

            # Calculate hours per week based on difficulty
            hours_per_week = {
                'Beginner': 5,
                'Intermediate': 8,
                'Advanced': 12
            }

            total_hours = sum(hours_per_week[course['difficulty']] * course['duration_weeks'] for course in recommended_courses)
            st.markdown(f"### 🕒 Total Estimated Study Hours: **{total_hours} hours**")

            # Weekly commitment recommendation
            st.markdown(f"### 📅 Recommended Weekly Commitment: **10-15 hours per week**")

    with tabs[3]:  # About Tab
        st.markdown('<div class="content-box">', unsafe_allow_html=True)
        st.markdown('<h2>About EduPathfinder</h2>', unsafe_allow_html=True)

        st.markdown("""
        <div class="info-box">
            <h3>Our Mission</h3>
            <p>
                EduPathfinder is dedicated to revolutionizing educational journeys by creating personalized learning paths
                that align with each student's unique learning style, interests, and career aspirations. We believe that
                education should be tailored to the individual, not the other way around.
            </p>
        </div>

        <div class="info-box">
            <h3>How It Works</h3>
            <p>Our advanced recommendation system uses a combination of:</p>
            <ul>
                <li><strong>Content-Based Filtering:</strong> Matching your interests and goals with course content</li>
                <li><strong>Collaborative Filtering:</strong> Learning from patterns of similar users</li>
                <li><strong>AI-Powered Analysis:</strong> Using Google's Gemini AI for intelligent recommendations</li>
                <li><strong>Learning Style Optimization:</strong> Adapting suggestions to your preferred learning methods</li>
            </ul>
        </div>

        <div class="info-box">
            <h3>Privacy and Data Usage</h3>
            <p>
                We value your privacy. Your learning data is used only to improve your recommendations and is never shared with third parties.
            </p>
        </div>

        <div class="info-box">
            <h3>Contact Us</h3>
            <p>
                For support or feedback, please contact us at:<br>
                <a href="mailto:support@edupathfinder.com">support@edupathfinder.com</a>
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
