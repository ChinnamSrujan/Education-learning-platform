# Education-learning-platform
A sophisticated personalized education path recommendation system that creates tailored learning journeys based on individual student profiles using advanced AI and data analytics.

EduPathfinder Banner

Key Features
Personalized Learning Paths based on:

Individual interests and preferences
Learning style assessment
Career goals and aspirations
Current experience level
Advanced Analytics Dashboard

Visual learning path timeline
Skills acquisition visualization
Curriculum breakdown analysis
Difficulty progression tracking
AI-Powered Recommendations

Content-based filtering using Gemini AI
Collaborative filtering algorithms
Learning style optimization
Career-aligned course suggestions
Comprehensive Course Information

Detailed course descriptions
Skills gained from each course
Prerequisites and difficulty levels
Career relevance insights
Professional User Interface

Modern, intuitive design
Responsive layout
Interactive visualizations
Tabbed navigation system
Implementation Details
AI Integration: Leverages Google's Gemini AI for intelligent recommendations
Data Visualization: Interactive charts using Altair and Matplotlib
User Session Management: Persistent user profiles and recommendation history
Learning Style Framework: VARK model integration (Visual, Auditory, Reading/Writing, Kinesthetic)
Setup
Clone this repository
Install the required dependencies:
pip install -r requirements.txt
Create a .env file in the root directory and add your Gemini API key:
GOOGLE_API_KEY=your_gemini_api_key_here
Get your API key from: https://makersuite.google.com/app/apikey
Running the Application
Make sure all dependencies are installed and the .env file is configured
Run the Streamlit app:
streamlit run app.py
Open your browser and navigate to the URL shown in the terminal (usually http://localhost:8501)
Usage
Create Your Profile

Enter your interests, learning style, and career goals
Set your current experience level
Save your profile
Generate Recommendations

Click "Generate Recommendations" to create your personalized learning path
View your course timeline and skill acquisition projections
Explore Course Details

Review detailed information about each recommended course
Understand why each course was recommended for you
See prerequisites and career relevance
Analyze Your Learning Journey

View analytics about your curriculum breakdown
Track difficulty progression throughout your path
See estimated completion time and study hour requirements
Technical Architecture
Frontend: Streamlit with custom CSS styling
Recommendation Engine: Hybrid system combining:
AI-powered content analysis
User profile matching
Career alignment algorithms
Data Management: Pandas for efficient data processing
Visualization: Altair and Matplotlib for interactive charts
Future Enhancements
User authentication system
Course completion tracking
Progress assessments
Social learning features
Integration with learning management systems
Mobile application
