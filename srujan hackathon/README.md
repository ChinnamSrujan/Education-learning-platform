# EduPathfinder: AI-Powered Learning Journey Platform

A sophisticated personalized education path recommendation system that creates tailored learning journeys based on individual student profiles using advanced AI and data analytics.

![EduPathfinder Banner](https://img.freepik.com/free-vector/gradient-online-courses-landing-page_23-2149038529.jpg?w=1380&t=st=1716559400~exp=1716560000~hmac=b576c92c9f0f77d6b4b13f82d5f83d1115ff72d6fe5e3a458b7f7cb33cd10afe)

## Key Features

- **Personalized Learning Paths** based on:
  - Individual interests and preferences
  - Learning style assessment
  - Career goals and aspirations
  - Current experience level
  
- **Advanced Analytics Dashboard**
  - Visual learning path timeline
  - Skills acquisition visualization
  - Curriculum breakdown analysis
  - Difficulty progression tracking
  
- **AI-Powered Recommendations**
  - Content-based filtering using Gemini AI
  - Collaborative filtering algorithms
  - Learning style optimization
  - Career-aligned course suggestions
  
- **Comprehensive Course Information**
  - Detailed course descriptions
  - Skills gained from each course
  - Prerequisites and difficulty levels
  - Career relevance insights
  
- **Professional User Interface**
  - Modern, intuitive design
  - Responsive layout
  - Interactive visualizations
  - Tabbed navigation system

## Implementation Details

- **AI Integration**: Leverages Google's Gemini AI for intelligent recommendations
- **Data Visualization**: Interactive charts using Altair and Matplotlib
- **User Session Management**: Persistent user profiles and recommendation history
- **Learning Style Framework**: VARK model integration (Visual, Auditory, Reading/Writing, Kinesthetic)

## Setup

1. Clone this repository
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root directory and add your Gemini API key:
   ```
   GOOGLE_API_KEY=your_gemini_api_key_here
   ```
   Get your API key from: https://makersuite.google.com/app/apikey

## Running the Application

1. Make sure all dependencies are installed and the `.env` file is configured
2. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```
3. Open your browser and navigate to the URL shown in the terminal (usually http://localhost:8501)

## Usage

1. **Create Your Profile**
   - Enter your interests, learning style, and career goals
   - Set your current experience level
   - Save your profile

2. **Generate Recommendations**
   - Click "Generate Recommendations" to create your personalized learning path
   - View your course timeline and skill acquisition projections

3. **Explore Course Details**
   - Review detailed information about each recommended course
   - Understand why each course was recommended for you
   - See prerequisites and career relevance

4. **Analyze Your Learning Journey**
   - View analytics about your curriculum breakdown
   - Track difficulty progression throughout your path
   - See estimated completion time and study hour requirements

## Technical Architecture

- **Frontend**: Streamlit with custom CSS styling
- **Recommendation Engine**: Hybrid system combining:
  - AI-powered content analysis
  - User profile matching
  - Career alignment algorithms
- **Data Management**: Pandas for efficient data processing
- **Visualization**: Altair and Matplotlib for interactive charts

## Future Enhancements

- User authentication system
- Course completion tracking
- Progress assessments
- Social learning features
- Integration with learning management systems
- Mobile application 