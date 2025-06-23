# Resume Matcher with Google Gemini and FastAPI

This project uses **FastAPI** and **Google Gemini** to build an AI-powered **Resume Matcher** web application. It helps automate the resume screening process by analyzing uploaded resumes and comparing them with a given job description. The results are returned with a match score and detailed analysis in a **clean, readable format**.

## 🚀 Features
- Upload **PDF** or **DOCX** resumes and a **Job Description**.
- **Google Gemini** analyzes the resumes and compares them with the job description.
- Results are displayed with a **match score** and a breakdown of relevant skills, experience, and education.
- Uses **Markdown** for structured, clean output, which is then rendered as HTML.
- User-friendly **FastAPI** backend with **Bootstrap** frontend.

## 🛠️ Technologies Used
- **Python 3.x**: The primary programming language.
- **FastAPI**: For building a fast and efficient backend API.
- **Uvicorn**: ASGI server for FastAPI.
- **Google Gemini API (google-generativeai)**: For natural language processing (NLP) and resume analysis.
- **PyPDF2**: For extracting text from PDF files.
- **python-docx**: For extracting text from DOCX files.
- **Markdown**: To structure the output of the AI model for display.
- **Jinja2**: For templating HTML pages.
- **python-dotenv**: For managing environment variables (like API keys).
- **Bootstrap 5**: For responsive and sleek UI design (via CDN in templates).



## Project Screenshots :

![Application Logo](https://raw.githubusercontent.com/MagicDash91/ML-Engineering-Project/main/Resume%20Screening%20with%20AI/static/h1.JPG)

![Application Logo](https://raw.githubusercontent.com/MagicDash91/ML-Engineering-Project/main/Resume%20Screening%20with%20AI/static/h2.JPG)

![Application Logo](https://raw.githubusercontent.com/MagicDash91/ML-Engineering-Project/main/Resume%20Screening%20with%20AI/static/h3.JPG)

![Application Logo](https://raw.githubusercontent.com/MagicDash91/ML-Engineering-Project/main/Resume%20Screening%20with%20AI/static/h4.JPG)

![Application Logo](https://raw.githubusercontent.com/MagicDash91/ML-Engineering-Project/main/Resume%20Screening%20with%20AI/static/h5.JPG)

![Application Logo](https://raw.githubusercontent.com/MagicDash91/ML-Engineering-Project/main/Resume%20Screening%20with%20AI/static/h6.JPG)

![Application Logo](https://raw.githubusercontent.com/MagicDash91/ML-Engineering-Project/main/Resume%20Screening%20with%20AI/static/h7.JPG)

## 🧑‍💻 Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone https://github.com/MagicDash91/ML-Engineering-Project.git
   cd resume-matcher
   ```

2. **Create a virtual environment:**

   ```bash
   python -m venv env
   source env/bin/activate  # For Linux/Mac
   env\Scripts\activate     # For Windows
   ```

3. **Install required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your Google API key:**
   - Create a file named `.env` in the root of the project.
   - Add your Google Gemini API key to this file as follows:
     ```
     GEMINI_API_KEY="YOUR_ACTUAL_API_KEY_HERE"
     ```
   - Replace `"YOUR_ACTUAL_API_KEY_HERE"` with your real API key.
   - The application uses `python-dotenv` to load this key from the `.env` file, so you don't need to modify `main.py` directly.

5. **Run the application:**
   ```bash
   uvicorn main:app --reload --port 9000
   ```
   The app will be running at http://127.0.0.1:9000.
   (Note: `main.py` is configured to use port 8000 by default if `PORT` env var is not set, but the original README mentioned 9000. Clarifying with `--port 9000` for consistency with the original README's instruction, or you can remove `--port 9000` to use the default 8000 or set the `PORT` environment variable.)

6. **Test the application:**
   Visit the link above and upload a job description along with resumes (PDF or DOCX format).

   The AI will analyze and provide match scores and feedback on each resume.

## 📝 Project Structure

```
resume-matcher/
├── .env                # Stores environment variables like API keys (Important: Add to .gitignore)
├── .gitignore          # Specifies intentionally untracked files that Git should ignore
├── main.py             # FastAPI app, routing logic, and core application code
├── requirements.txt    # Required Python dependencies
├── static/
│   ├── css/
│   │   └── style.css   # Custom stylesheets
│   └── (uploaded files might be temporarily stored here or in UPLOAD_DIR if configured)
├── templates/
│   ├── error.html      # HTML template for error pages
│   ├── index.html      # HTML template for the main upload page
│   └── results.html    # HTML template for displaying analysis results
├── README.md           # This file
└── __pycache__/        # Python bytecode cache (Usually gitignored)

```
*Note: The `UPLOAD_DIR` ("temp_uploads") is created by `main.py` for temporary file storage during processing but might not be present if the app hasn't run or processed files yet. It's also a good candidate for `.gitignore`.*

## 🤖 How It Works
1.  **Upload Resumes**: Users can upload multiple resumes in PDF or DOCX format.
2.  **Job Description**: Users input a job description that the resumes will be evaluated against.
3.  **Google Gemini Model**: The Google Gemini API is used to analyze how well the resume matches the job description. The system scores each resume and provides a detailed explanation.
4.  **Results**: The results are displayed as a clean list, where each resume is scored along with the breakdown of relevant skills and experiences.

## 📄 Example Results
After analysis, the application will return the results in the following format:

**Candidate 1**
**Score: 8/10**
**Explanation:** The candidate has relevant skills and experience in Python, Data Science, and Machine Learning. However, they are missing some specific experience with SQL databases.

**Candidate 2**
**Score: 6/10**
**Explanation:** The candidate has some experience with data analysis but lacks key qualifications in machine learning and data engineering.

## 💡 Contributing
Feel free to fork the repository, make changes, and create pull requests. Contributions are always welcome!

## 🤝 License
This project is licensed under the MIT License - see the `LICENSE` file for details.
