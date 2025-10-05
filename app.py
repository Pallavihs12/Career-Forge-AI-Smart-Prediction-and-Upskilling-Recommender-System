# --- Imports ---
from flask import Flask, render_template, send_file, redirect, request, session, url_for, flash, jsonify
import os
import json
import base64
import string
import fitz
import random
from mistralai import Mistral
import mysql.connector
import requests
import shutil
from datetime import timedelta
import googleapiclient.discovery
import googleapiclient.errors

app = Flask(__name__)
app.secret_key = ".env"

# Database Configuration
try:
    link = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='skillgap_2025'
    )
    print("Database connection successful")
except mysql.connector.Error as err:
    print(f"FATAL: Error connecting to database: {err}")
    print("Authentication features will fail. Please check DB connection details.")
    link = None

# AI Configuration
mistral_api_key = "WTuMOibXWmpTqjvscYHSaaCOjjXCakkJ"
mistral_model = "pixtral-large-2411"
try:
    client = Mistral(api_key=mistral_api_key)
    print("Mistral client initialized")
except Exception as e:
    print(f"FATAL: Error initializing Mistral client: {e}")
    client = None

# Job API Configuration
ADZUNA_APP_ID = "your_adzuna_app_id"
ADZUNA_APP_KEY = "your_adzuna_app_key"

# YouTube API Configuration
YOUTUBE_API_KEY = "your_youtube_api_key"
try:
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    print("YouTube API client built successfully.")
except Exception as build_error:
    print(f"FATAL: Error building YouTube API client: {build_error}")
    youtube = None

class SkillGapAnalysis:
    """Class to hold skill gap analysis results"""
    def __init__(self, resume_skills, required_skills, missing_skills):
        self.resume_skills = resume_skills
        self.required_skills = required_skills
        self.missing_skills = missing_skills

@app.after_request
def add_header(response):
    """Add headers to prevent caching"""
    response.cache_control.no_store = True
    return response

def encode_image(image_filepath):
    """Reads an image file and returns its Base64 encoded string"""
    try:
        with open(image_filepath, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    except Exception as e:
        print(f"Error encoding image {image_filepath}: {e}")
        return None

def pdf_to_images(pdf_filepath, output_folder):
    """Converts each page of a PDF to a PNG image"""
    output_images = []
    try:
        doc = fitz.open(pdf_filepath)
        zoom = 2
        mat = fitz.Matrix(zoom, zoom)
        print(f"Processing PDF: {os.path.basename(pdf_filepath)}, Pages: {len(doc)}")
        
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            pix = page.get_pixmap(matrix=mat)
            image_filename = f"page_{page_num+1}.png"
            image_filepath = os.path.join(output_folder, image_filename)
            pix.save(image_filepath)
            output_images.append(image_filepath)
        doc.close()
        print(f"Converted PDF to {len(output_images)} images")
    except Exception as e:
        print(f"Error converting PDF {pdf_filepath} to images: {e}")
    return output_images

def extract_keywords_from_image(image_filepath):
    """Uses Mistral API to extract skills from a resume image with improved accuracy"""
    if not client:
        print("Mistral client not initialized")
        return []

    image_base64 = encode_image(image_filepath)
    if not image_base64:
        return []

    prompt = (
        "Analyze this resume image carefully and extract ALL technical skills, programming languages, "
        "frameworks, tools, technologies, certifications, and relevant professional skills mentioned. "
        "Look for:\n"
        "- Programming languages (Python, Java, JavaScript, C++, etc.)\n"
        "- Frameworks and libraries (React, Angular, Django, Spring, etc.)\n"
        "- Databases (MySQL, PostgreSQL, MongoDB, etc.)\n"
        "- Cloud platforms (AWS, Azure, GCP, etc.)\n"
        "- Tools and software (Git, Docker, Jenkins, etc.)\n"
        "- Technical methodologies (Agile, DevOps, etc.)\n"
        "- Certifications and qualifications\n"
        "- Domain-specific skills\n\n"
        "Be thorough and include variations (e.g., 'JS' and 'JavaScript'). "
        "Return ONLY a JSON object with a single key 'keywords' containing a comprehensive list of strings. "
        "Include both exact matches and common abbreviations/variations."
    )
    
    messages = [{
        "role": "user",
        "content": [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": f"data:image/png;base64,{image_base64}"}
        ]
    }]
    
    try:
        chat_response = client.chat.complete(
            model=mistral_model,
            messages=messages,
            response_format={"type": "json_object"}
        )
        extracted_text = chat_response.choices[0].message.content
        
        try:
            result = json.loads(extracted_text)
            keywords = result.get("keywords", [])
            # Clean and normalize keywords
            cleaned_keywords = []
            for k in keywords:
                if k and k.strip():
                    # Remove common non-skill words and normalize
                    skill = k.strip().lower()
                    if len(skill) > 1 and skill not in ['and', 'or', 'the', 'with', 'using', 'experience', 'knowledge']:
                        cleaned_keywords.append(skill.title())
            return list(set(cleaned_keywords))  # Remove duplicates
        except json.JSONDecodeError:
            print(f"Could not parse JSON response: {extracted_text}")
            return []
    except Exception as e:
        print(f"Error during Mistral API call: {e}")
        return []

def analyze_skill_gap(resume_skills, job_designation):
    """Analyzes the gap between resume skills and job requirements"""
    if not client:
        print("Mistral client not available for skill gap analysis")
        return None

    prompt = (
        f"Analyze the skill gap between these resume skills and a {job_designation} role.\n"
        f"Resume Skills: {', '.join(resume_skills)}\n\n"
        "Return a JSON object with these keys:\n"
        "'resume_skills' (array of relevant skills from resume),\n"
        "'required_skills' (array of typical skills needed for this job),\n"
        "'missing_skills' (array of skills needed but not in resume).\n"
        "Only include technical and job-relevant skills."
    )
    
    try:
        messages = [{"role": "user", "content": prompt}]
        chat_response = client.chat.complete(
            model=mistral_model,
            messages=messages,
            response_format={"type": "json_object"}
        )
        response_content = chat_response.choices[0].message.content
        
        try:
            # Try to parse the response directly
            result = json.loads(response_content)
            return SkillGapAnalysis(
                resume_skills=result.get('resume_skills', []),
                required_skills=result.get('required_skills', []),
                missing_skills=result.get('missing_skills', [])
            )
        except json.JSONDecodeError:
            # Fallback parsing if response isn't clean JSON
            data_start = response_content.find('{')
            data_end = response_content.rfind('}') + 1
            if data_start != -1 and data_end != -1:
                json_str = response_content[data_start:data_end]
                result = json.loads(json_str)
                return SkillGapAnalysis(
                    resume_skills=result.get('resume_skills', []),
                    required_skills=result.get('required_skills', []),
                    missing_skills=result.get('missing_skills', [])
                )
            return None
    except Exception as e:
        print(f"Error during skill gap analysis: {e}")
        return None

def get_job_recommendations(keywords, location="bengaluru", results_per_keyword=2):
    """Gets job recommendations from Adzuna API"""
    if not ADZUNA_APP_ID or not ADZUNA_APP_KEY:
        print("Adzuna credentials not configured")
        return []
    
    jobs = []
    for keyword in keywords[:3]:  # Limit to top 3 keywords
        try:
            url = (
                f"https://api.adzuna.com/v1/api/jobs/in/search/1?"
                f"app_id={ADZUNA_APP_ID}&app_key={ADZUNA_APP_KEY}"
                f"&results_per_page={results_per_keyword}"
                f"&what={requests.utils.quote(keyword)}"
                f"&where={location}&content-type=application/json"
            )
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            jobs.extend(response.json().get('results', []))
        except Exception as e:
            print(f"Error fetching jobs for {keyword}: {e}")
    return jobs

def get_video_tutorials(keywords, max_results=2):
    """Gets relevant video tutorials from YouTube"""
    if not youtube:
        print("YouTube client not available")
        return {}
    
    tutorials = {}
    for keyword in keywords[:5]:  # Limit to top 5 keywords
        try:
            search_response = youtube.search().list(
                q=f"{keyword} tutorial",
                part="id,snippet",
                maxResults=max_results,
                type="video",
                order="relevance"
            ).execute()
            
            video_list = []
            for item in search_response.get("items", []):
                video_id = item["id"].get("videoId")
                video_title = item["snippet"].get("title")
                if video_id and video_title:
                    video_list.append({
                        "title": video_title,
                        "link": f"https://www.youtube.com/watch?v={video_id}"
                    })
            
            if video_list:
                tutorials[keyword.lower()] = video_list
        except Exception as e:
            print(f"Error fetching videos for {keyword}: {e}")
    return tutorials

# --- Routes ---
@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('userhome'))
    return render_template('index.html')

@app.route('/ulogin', methods=['GET', 'POST'])
def ulogin():
    if not link or not link.is_connected():
        flash('Database connection failed', 'error')
        return render_template('ulogin.html')

    if 'user' in session:
        return redirect(url_for('userhome'))

    if request.method == "GET":
        return render_template('ulogin.html')

    try:
        cursor = link.cursor(dictionary=True)
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            flash('Email and password are required', 'warning')
            return redirect(url_for('ulogin'))

        cursor.execute("SELECT uid, name FROM skillgap_2025_user WHERE email = %s AND password = %s", 
                      (email, password))
        user = cursor.fetchone()

        if user:
            session['user'] = user['uid']
            session['username'] = user['name']
            session.permanent = True
            app.permanent_session_lifetime = timedelta(days=7)
            return redirect(url_for('userhome'))
        else:
            flash('Invalid email or password', 'error')
            return render_template('ulogin.html')
    except Exception as e:
        print(f"Login error: {e}")
        flash('An error occurred during login', 'error')
        return render_template('ulogin.html')

@app.route('/uregister', methods=['GET', 'POST'])
def uregister():
    if not link or not link.is_connected():
        flash('Database connection failed', 'error')
        return render_template('uregister.html')

    if 'user' in session:
        return redirect(url_for('userhome'))

    if request.method == "GET":
        return render_template('uregister.html')

    try:
        cursor = link.cursor()
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        phone = request.form.get("phone")

        if not all([name, email, password, phone]):
            flash('All fields are required', 'warning')
            return render_template('uregister.html')

        cursor.execute("SELECT email FROM skillgap_2025_user WHERE email = %s", (email,))
        if cursor.fetchone():
            flash('Email already exists', 'warning')
            return render_template('uregister.html')

        uid_val = 'user_' + ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        insert_sql = "INSERT INTO skillgap_2025_user (uid, name, email, password, phone) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(insert_sql, (uid_val, name, email, password, phone))
        link.commit()
        
        flash('Registration successful! Please login', 'success')
        return redirect(url_for('ulogin'))
    except Exception as e:
        print(f"Registration error: {e}")
        link.rollback()
        flash('An error occurred during registration', 'error')
        return render_template('uregister.html')

@app.route('/userhome')
def userhome():
    if 'user' not in session:
        flash("Please login", "warning")
        return redirect(url_for('ulogin'))
    return render_template('userhome.html', username=session.get('username', 'User'))

@app.route('/ulogout')
def ulogout():
    session.pop('user', None)
    session.pop('username', None)
    flash('Logged out successfully', 'info')
    return redirect(url_for('ulogin'))

@app.route('/upload', methods=["GET", "POST"])
def upload():
    if 'user' not in session:
        flash("Please login to upload a resume", "warning")
        return redirect(url_for('ulogin'))

    if request.method == "GET":
        return render_template('upload.html', 
                           job_results=None, 
                           video_tutorials=None,
                           skill_gap_analysis=None,
                           job_designation=None)

    # Validate file upload
    if 'file' not in request.files:
        flash("No file selected", "error")
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        flash("No file selected", "error")
        return redirect(request.url)
    if not file.filename.lower().endswith('.pdf'):
        flash("Only PDF files are allowed", "error")
        return redirect(request.url)

    # Validate job designation
    job_designation = request.form.get('job_designation', '').strip()
    if not job_designation:
        flash("Please enter a job designation", "error")
        return redirect(request.url)

    # Create processing workspace
    processing_uid = 'proc_' + ''.join(random.choices(string.ascii_letters + string.digits, k=12))
    base_folder = os.path.join("workspace", processing_uid)
    pdf_folder = os.path.join(base_folder, "pdf")
    image_folder = os.path.join(base_folder, "images")
    os.makedirs(pdf_folder, exist_ok=True)
    os.makedirs(image_folder, exist_ok=True)

    pdf_filepath = os.path.join(pdf_folder, file.filename)
    
    try:
        # Save and process the PDF
        file.save(pdf_filepath)
        page_images = pdf_to_images(pdf_filepath, image_folder)
        if not page_images:
            raise ValueError("Failed to convert PDF to images")

        # Extract skills from resume
        all_keywords = set()
        if client:
            print(f"Processing {len(page_images)} pages for skill extraction...")
            for img_path in page_images:
                extracted_kw = extract_keywords_from_image(img_path)
                if extracted_kw:
                    # Keep original case for better presentation
                    all_keywords.update(extracted_kw)
            final_keywords = sorted(list(all_keywords))
            print(f"Extracted {len(final_keywords)} skills: {final_keywords}")
        else:
            final_keywords = []
            flash("AI service unavailable - limited functionality", "warning")

        # Perform skill gap analysis
        skill_gap = analyze_skill_gap(final_keywords, job_designation) if final_keywords else None

        # Get recommendations based on missing skills
        missing_skills = skill_gap.missing_skills if skill_gap else []
        job_results = get_job_recommendations(missing_skills or final_keywords) if (missing_skills or final_keywords) else []
        video_tutorials = get_video_tutorials(missing_skills) if missing_skills else {}

        # Success message with details
        success_msg = f"Resume uploaded and analyzed successfully! Found {len(final_keywords)} skills."
        
        return render_template('upload.html',
                           success=success_msg,
                           job_results=job_results,
                           video_tutorials=video_tutorials,
                           skill_gap_analysis=skill_gap,
                           job_designation=job_designation,
                           resume_uploaded=True)

    except ValueError as ve:
        flash(f"Processing error: {ve}", "error")
        return redirect(url_for('upload'))
    except Exception as e:
        print(f"Upload error: {e}")
        flash("An error occurred during processing", "error")
        return redirect(url_for('upload'))
    finally:
        # Clean up workspace
        if os.path.exists(base_folder):
            try:
                shutil.rmtree(base_folder)
            except Exception as e:
                print(f"Error cleaning up workspace: {e}")

# --- Quiz Routes (Keep all your original quiz routes exactly as they were) ---
@app.route('/quiz/<segment>', methods=['GET'])
def quiz(segment):
    if 'user' not in session:
        flash("Please login to take a quiz.", "warning")
        return redirect(url_for('ulogin'))

    if not link or not link.is_connected():
        flash('Database connection failed. Cannot load quiz.', 'error')
        return redirect(url_for('userhome'))

    cursor = None
    questions = []
    try:
        cursor = link.cursor(dictionary=True)
        cursor.execute("SELECT uid, question_text, option_a, option_b, option_c, option_d, correct_answer FROM skillgap_2025_questions WHERE segment = %s", (segment,))
        questions = cursor.fetchall()

        if not questions:
            flash(f"No questions found for segment: {segment}", "warning")
            return redirect(url_for('userhome'))

    except mysql.connector.Error as db_err:
        print(f"Quiz load DB error for segment {segment}: {db_err}")
        flash('Database error loading quiz questions. Please try again.', 'error')
        return redirect(url_for('userhome'))
    except Exception as e:
        print(f"Quiz load general error for segment {segment}: {e}")
        flash('An unexpected error occurred loading the quiz.', 'error')
        return redirect(url_for('userhome'))
    finally:
        if cursor: cursor.close()

    return render_template('quiz.html', segment=segment, questions=questions)

@app.route('/submit_quiz', methods=['POST'])
def submit_quiz():
    if 'user' not in session:
        flash("Please login to submit a quiz.", "warning")
        return redirect(url_for('ulogin'))

    if not link or not link.is_connected():
        flash('Database connection failed. Cannot submit quiz.', 'error')
        return redirect(url_for('userhome'))

    user_uid = session['user']
    segment = request.form.get('segment')
    score = 0
    total_questions = 0
    result_id = None

    cursor = None
    try:
        cursor = link.cursor()

        insert_result_sql = "INSERT INTO skillgap_2025_result (user_uid, segment, score) VALUES (%s, %s, %s)"
        cursor.execute(insert_result_sql, (user_uid, segment, score))
        link.commit()
        result_id = cursor.lastrowid

        insert_item_sql = "INSERT INTO skillgap_2025_resultitems (result_id, question_uid, correct_answer, user_answer) VALUES (%s, %s, %s, %s)"
        result_items_data = []

        for key, value in request.form.items():
            if key.startswith('answer_'):
                question_uid = key.replace('answer_', '')
                user_answer = value
                correct_answer_key = f'question_{question_uid}_correct_answer'
                correct_answer = request.form.get(correct_answer_key)

                if correct_answer is not None:
                    total_questions += 1
                    if user_answer == correct_answer:
                        score += 1
                    result_items_data.append((result_id, question_uid, correct_answer, user_answer))

        if result_items_data:
            cursor.executemany(insert_item_sql, result_items_data)
            link.commit()

        update_result_sql = "UPDATE skillgap_2025_result SET score = %s WHERE id = %s"
        cursor.execute(update_result_sql, (score, result_id))
        link.commit()

        return redirect(url_for('result', result_id=result_id))

    except mysql.connector.Error as db_err:
        print(f"Quiz submission DB error: {db_err}")
        link.rollback()
        flash('Database error during quiz submission. Please try again.', 'error')
        if segment:
            return redirect(url_for('quiz', segment=segment))
        else:
            return redirect(url_for('userhome'))
    except Exception as e:
        print(f"Quiz submission general error: {e}")
        link.rollback()
        flash('An unexpected error occurred during quiz submission.', 'error')
        if segment:
            return redirect(url_for('quiz', segment=segment))
        else:
            return redirect(url_for('userhome'))
    finally:
        if cursor: cursor.close()

@app.route('/result/<int:result_id>', methods=['GET'])
def result(result_id):
    if 'user' not in session:
        flash("Please login to view quiz results.", "warning")
        return redirect(url_for('ulogin'))

    if not link or not link.is_connected():
        flash('Database connection failed. Cannot load result.', 'error')
        return redirect(url_for('userhome'))

    cursor = None
    result_data = None
    total_questions = 0
    recommended_videos = []

    try:
        cursor = link.cursor(dictionary=True)

        cursor.execute("SELECT segment, score FROM skillgap_2025_result WHERE id = %s AND user_uid = %s", (result_id, session['user']))
        result_data = cursor.fetchone()

        if not result_data:
            flash("Result not found or you do not have permission to view it.", "error")
            return redirect(url_for('userhome'))

        cursor.execute("SELECT COUNT(*) AS total FROM skillgap_2025_resultitems WHERE result_id = %s", (result_id,))
        count_row = cursor.fetchone()
        if count_row:
            total_questions = count_row['total']

        score = result_data['score']
        segment = result_data['segment']
        percentage_score = (score / total_questions) * 100 if total_questions > 0 else 0

        num_videos = 0
        if percentage_score < 50:
            num_videos = 3
        elif 50 <= percentage_score < 60:
            num_videos = 2
        elif 60 <= percentage_score < 80:
            num_videos = 1

        if num_videos > 0 and youtube:
            print(f"Fetching {num_videos} video tutorials for segment: {segment} (Quiz Result feature)...")
            search_query = f"{segment} tutorial"

            try:
                search_response = youtube.search().list(
                    q=search_query,
                    part="id,snippet",
                    maxResults=num_videos,
                    type="video",
                    order="relevance"
                ).execute()

                tutorials_list = []
                for item in search_response.get("items", []):
                    video_id = item["id"].get("videoId")
                    video_title = item["snippet"].get("title")
                    if video_id and video_title:
                        video_link = f"https://www.youtube.com/watch?v={video_id}"
                        tutorials_list.append({"title": video_title, "link": video_link})

                recommended_videos = tutorials_list
            except Exception as e:
                print(f"Error fetching YouTube videos: {e}")

        return render_template('result.html',
                           segment=segment,
                           score=score,
                           total_questions=total_questions,
                           percentage_score=percentage_score,
                           recommended_videos=recommended_videos)

    except mysql.connector.Error as db_err:
        print(f"Result load DB error for result ID {result_id}: {db_err}")
        flash('Database error loading result. Please try again.', 'error')
        return redirect(url_for('userhome'))
    except Exception as e:
        print(f"Result load general error for result ID {result_id}: {e}")
        flash('An unexpected error occurred loading the result.', 'error')
        return redirect(url_for('userhome'))
    finally:
        if cursor: cursor.close()

@app.route('/quizhistory', methods=['GET'])
def quiz_history():
    if 'user' not in session:
        flash("Please login to view quiz history.", "warning")
        return redirect(url_for('ulogin'))

    if not link or not link.is_connected():
        flash('Database connection failed. Cannot load quiz history.', 'error')
        return redirect(url_for('userhome'))

    user_uid = session['user']
    quiz_results = []
    cursor = None
    try:
        cursor = link.cursor(dictionary=True)
        cursor.execute("SELECT id, segment, score, timestamp FROM skillgap_2025_result WHERE user_uid = %s ORDER BY timestamp DESC", (user_uid,))
        quiz_results = cursor.fetchall()

    except mysql.connector.Error as db_err:
        print(f"Quiz history load DB error for user {user_uid}: {db_err}")
        flash('Database error loading quiz history. Please try again.', 'error')
        return redirect(url_for('userhome'))
    except Exception as e:
        print(f"Quiz history load general error for user {user_uid}: {e}")
        flash('An unexpected error occurred loading quiz history.', 'error')
        return redirect(url_for('userhome'))
    finally:
        if cursor: cursor.close()

    return render_template('quizhistory.html', quiz_results=quiz_results)

@app.route('/quizitems/<int:result_id>', methods=['GET'])
def quiz_items(result_id):
    if 'user' not in session:
        flash("Please login to view quiz details.", "warning")
        return redirect(url_for('ulogin'))

    if not link or not link.is_connected():
        flash('Database connection failed. Cannot load quiz details.', 'error')
        return redirect(url_for('quiz_history'))

    user_uid = session['user']
    quiz_items_data = []
    result_exists = False
    cursor = None
    try:
        cursor = link.cursor(dictionary=True)

        cursor.execute("SELECT id FROM skillgap_2025_result WHERE id = %s AND user_uid = %s", (result_id, user_uid))
        if cursor.fetchone():
            result_exists = True
            cursor.execute("""
                SELECT
                    qi.correct_answer,
                    qi.user_answer,
                    q.question_text
                FROM skillgap_2025_resultitems qi
                JOIN skillgap_2025_questions q ON qi.question_uid = q.uid
                WHERE qi.result_id = %s
            """, (result_id,))
            quiz_items_data = cursor.fetchall()
        else:
            flash("Quiz result not found or you do not have permission to view it.", "error")
            return redirect(url_for('quiz_history'))

    except mysql.connector.Error as db_err:
        print(f"Quiz items load DB error for result ID {result_id}: {db_err}")
        flash('Database error loading quiz details. Please try again.', 'error')
        return redirect(url_for('quiz_history'))
    except Exception as e:
        print(f"Quiz items load general error for result ID {result_id}: {e}")
        flash('An unexpected error occurred loading quiz details.', 'error')
        return redirect(url_for('quiz_history'))
    finally:
        if cursor: cursor.close()

    if result_exists:
        return render_template('quizitems.html', result_id=result_id, quiz_items=quiz_items_data)
    else:
        flash("Could not retrieve quiz details.", "error")
        return redirect(url_for('quiz_history'))

if __name__ == "__main__":
    if not os.path.exists("workspace"):
        os.makedirs("workspace")

    app.run(host='0.0.0.0', port=5000, debug=True)
