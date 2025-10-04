# Upskills Recommendation System

## Overview

The Upskills Recommendation System is a comprehensive web application built with Flask that helps users identify skill gaps in their resumes and provides personalized recommendations for career development. The system combines AI-powered resume analysis with interactive quizzes and learning resources to guide users in their professional growth.

## Key Features

### 🔍 AI-Powered Resume Analysis
- **PDF Resume Processing**: Upload and analyze PDF resumes using PyMuPDF
- **Skill Extraction**: Uses Mistral AI (Pixtral Large 2411) to extract skills, technologies, and job titles from resume images
- **Skill Gap Analysis**: Compares resume skills against job requirements to identify missing competencies
- **Job Recommendations**: Fetches relevant job opportunities from Adzuna API based on skill gaps
- **Learning Resources**: Provides YouTube tutorial recommendations for skill development

### 📝 Interactive Quiz System
- **Multi-Category Quizzes**: Covers Mathematics, Aptitude, C++, and Computer Science
- **Personalized Learning**: Recommends video tutorials based on quiz performance
- **Progress Tracking**: Maintains quiz history and detailed result analysis
- **Performance-Based Recommendations**: 
  - Score < 50%: 3 tutorial videos
  - Score 50-60%: 2 tutorial videos  
  - Score 60-80%: 1 tutorial video
  - Score > 80%: No additional tutorials needed

### 👤 User Management
- **User Registration & Authentication**: Secure user accounts with session management
- **Profile Management**: User data storage and retrieval
- **Session Persistence**: 7-day session lifetime for user convenience

## Technology Stack

### Backend
- **Framework**: Flask (Python)
- **Database**: MySQL with mysql-connector-python
- **AI Integration**: Mistral AI API for resume analysis
- **PDF Processing**: PyMuPDF (fitz) for document conversion
- **External APIs**: 
  - Adzuna API for job recommendations
  - YouTube Data API v3 for tutorial videos

### Frontend
- **Templates**: Jinja2 templating engine
- **Styling**: Bootstrap CSS framework
- **Icons**: Font Awesome
- **JavaScript**: jQuery and Bootstrap JS

### Dependencies
```
Flask
PyMuPDF
mistralai
mysql-connector-python
requests
google-api-python-client
```

## Database Schema

### Tables
1. **skillgap_2025_user**: User account information
2. **skillgap_2025_questions**: Quiz questions with multiple choice options
3. **skillgap_2025_result**: Quiz results and scores
4. **skillgap_2025_resultitems**: Detailed quiz responses
5. **skillgap_2025_data**: Additional user data storage

### Key Relationships
- Users can take multiple quizzes (one-to-many)
- Quiz results link to detailed question responses
- Foreign key constraints ensure data integrity

## Application Architecture

### Core Components

#### 1. Resume Processing Pipeline
```
PDF Upload → Image Conversion → AI Analysis → Skill Extraction → Gap Analysis
```

#### 2. Skill Gap Analysis Class
```python
class SkillGapAnalysis:
    - resume_skills: Skills found in resume
    - required_skills: Skills needed for target job
    - missing_skills: Skills to develop
```

#### 3. API Integrations
- **Mistral AI**: Resume text extraction and skill analysis
- **Adzuna**: Job market data and recommendations
- **YouTube**: Educational content discovery

### File Structure
```
e:\Upskills Recommendation/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── skillgap_2025.sql     # Database schema
├── SkillMorphQuestions.csv # Quiz questions data
├── cmd1.bat              # Application launcher
├── templates/            # HTML templates
│   ├── index.html        # Landing page
│   ├── ulogin.html       # User login
│   ├── uregister.html    # User registration
│   ├── userhome.html     # User dashboard
│   ├── upload.html       # Resume upload & analysis
│   ├── quiz.html         # Quiz interface
│   ├── result.html       # Quiz results
│   ├── quizhistory.html  # Quiz history
│   └── quizitems.html    # Detailed quiz review
├── static/               # Static assets
│   ├── css/              # Stylesheets
│   ├── js/               # JavaScript files
│   └── images/           # Application images
└── workspace/            # Temporary file processing
```

## Installation & Setup

### Prerequisites
- Python 3.7+
- MySQL Server
- API Keys for:
  - Mistral AI
  - Adzuna Jobs API
  - YouTube Data API v3

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd "Upskills Recommendation"
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Database Setup**
   ```bash
   mysql -u root -p < skillgap_2025.sql
   ```

4. **Configure API Keys**
   Update the following variables in `app.py`:
   ```python
   mistral_api_key = "your_mistral_api_key"
   ADZUNA_APP_ID = "your_adzuna_app_id"
   ADZUNA_APP_KEY = "your_adzuna_app_key"
   YOUTUBE_API_KEY = "your_youtube_api_key"
   ```

5. **Database Configuration**
   Update database connection details in `app.py`:
   ```python
   link = mysql.connector.connect(
       host='localhost',
       user='root',
       password='your_password',
       database='skillgap_2025'
   )
   ```

### Running the Application

#### Method 1: Using Flask CLI
```bash
set FLASK_APP=app.py
flask run -p 3200
```

#### Method 2: Using Batch File
```bash
cmd1.bat
```

#### Method 3: Direct Python Execution
```bash
python app.py
```

The application will be available at `http://localhost:5000` (or port 3200 if using Flask CLI).

## Usage Guide

### For Job Seekers

1. **Register/Login**: Create an account or log in to existing account
2. **Upload Resume**: Upload PDF resume for analysis
3. **Specify Job Role**: Enter target job designation
4. **Review Analysis**: View skill gaps and recommendations
5. **Take Quizzes**: Assess knowledge in various domains
6. **Access Resources**: Use recommended tutorials and job listings

### For Skill Development

1. **Skill Gap Identification**: System identifies missing skills for target roles
2. **Personalized Learning**: Receive YouTube tutorials based on skill gaps
3. **Progress Tracking**: Monitor improvement through quiz history
4. **Job Market Insights**: Access relevant job opportunities

## API Endpoints

### Authentication Routes
- `GET/POST /ulogin` - User login
- `GET/POST /uregister` - User registration
- `GET /ulogout` - User logout

### Core Features
- `GET /` - Landing page
- `GET /userhome` - User dashboard
- `GET/POST /upload` - Resume upload and analysis

### Quiz System
- `GET /quiz/<segment>` - Take quiz by category
- `POST /submit_quiz` - Submit quiz responses
- `GET /result/<result_id>` - View quiz results
- `GET /quizhistory` - View quiz history
- `GET /quizitems/<result_id>` - Detailed quiz review

## Security Features

- **Session Management**: Secure session handling with 7-day persistence
- **Input Validation**: Form data validation and sanitization
- **Error Handling**: Comprehensive error handling and user feedback
- **Database Security**: Parameterized queries to prevent SQL injection
- **File Upload Security**: PDF-only uploads with validation

## Performance Optimizations

- **Temporary Workspace**: Automatic cleanup of processing files
- **API Rate Limiting**: Controlled API calls to external services
- **Database Indexing**: Optimized database queries with proper indexing
- **Caching Headers**: No-cache headers for dynamic content

## Future Enhancements

### Planned Features
- **Multi-format Resume Support**: Support for DOC, DOCX formats
- **Advanced Analytics**: Detailed skill trend analysis
- **Certification Tracking**: Integration with certification platforms
- **Mobile Application**: React Native mobile app
- **Machine Learning**: Improved skill matching algorithms

### Technical Improvements
- **Containerization**: Docker deployment support
- **Cloud Integration**: AWS/Azure deployment options
- **API Documentation**: Swagger/OpenAPI documentation
- **Testing Suite**: Comprehensive unit and integration tests
- **Monitoring**: Application performance monitoring

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation for common solutions

## Acknowledgments

- **Mistral AI** for advanced resume analysis capabilities
- **Adzuna** for job market data
- **YouTube Data API** for educational content
- **Bootstrap** for responsive UI components
- **Flask** community for excellent documentation and support

---

*Last Updated: January 2025*