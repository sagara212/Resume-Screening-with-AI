import os
from dotenv import load_dotenv

load_dotenv()  # <-- Pindahkan ke sini, sebelum os.getenv

import uuid
import asyncio
from typing import List, Dict, Any
from pathlib import Path
import json
import logging

from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import google.generativeai as genai
import markdown

#document processing libraries
import PyPDF2
from docx import Document 
import pandas as pd
from io import BytesIO


app = FastAPI()

#Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="static/templates")

# Configuration
GEMINI_MODEL =  "gemini-2.0-flash"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
UPLOAD_DIR = "temp_uploads"

#Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Ensure directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs('static', exist_ok=True)
os.makedirs('templates', exist_ok=True)

class DocumentProcessor:
    """Handle document loading and text extraction"""
    
    @staticmethod
    def extract_text_from_pdf(file_content: bytes) -> str:
        """Extract text from PDF file"""
        try:
            reader = PyPDF2.PdfReader(BytesIO(file_content))
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            logging.error(f"Error extracting text from PDF: {e}")
            return ""
    
    @staticmethod
    def extract_text_from_docx(file_content: bytes) -> str:
         """Extract text from DOCX file"""
         try:
             doc = Document(BytesIO(file_content))
             text = ""
             for paragraph in doc.paragraphs:
                 text += paragraph.text + "\n"
             return text.strip()
         except Exception as e:
             logging.error(f"Error extracting text from DOCX: {e}")
             return ""
    
    def process_file(self, file_content: bytes, filename:str) -> str:
        """Process file based on extension"""
        file_ext = Path(filename).suffix.lower()

        if file_ext == ".pdf":
            return self.extract_text_from_pdf(file_content)
        elif file_ext == ".docx":
            return self.extract_text_from_docx(file_content)
        elif file_ext == ".txt":
            return file_content.decode("utf-8")
        else:
            raise HTTPException(f"Unsupported file type: {file_ext}. Only PDF and DOCX are supported.")
        

class ResumeAnalyzer:
    """Handle resume analysis using Gemini AI"""
    def __init__(self):
        self.model = genai.GenerativeModel(GEMINI_MODEL)
        self.analysis_prompt_template = """

Anda adalah konsultan HR ahli dan career coach yang berspesialisasi dalam optimasi CV dan analisis pasar kerja Indonesia. Tugas Anda adalah memberikan feedback komprehensif dan actionable untuk membantu pencari kerja meningkatkan CV mereka secara signifikan untuk peluang kerja yang spesifik.

## Informasi Input:
**Deskripsi Pekerjaan:**
{job_description}

**CV/Resume Saat Ini:**
{resume_content}

## Framework Analisis:

### 1. PENILAIAN KESESUAIAN
- Hitung persentase kecocokan berdasarkan requirement pekerjaan vs. isi CV
- Identifikasi keselarasan kata kunci dengan job description
- Evaluasi kompatibilitas dengan sistem ATS (Applicant Tracking System)
- Analisis demonstrasi kompetensi yang relevan dengan posisi

### 2. ANALISIS MENDALAM
Periksa area kritis berikut:
- **Skill Teknis:** Hard skills, sertifikasi, kemampuan software
- **Soft Skills:** Kepemimpinan, komunikasi, problem solving dengan bukti konkret
- **Relevansi Pengalaman:** Progres karir, kuantifikasi pencapaian, keselarasan industri
- **Pendidikan & Kredensial:** Relevansi gelar, sertifikasi tambahan, continuous learning
- **Presentasi Profesional:** Format, struktur, keterbacaan, bahasa profesional

### 3. IDENTIFIKASI GAP
- Requirement yang hilang dari job description
- Pengalaman yang kurang ditonjolkan padahal bisa lebih dihighlight
- Skill yang ada tapi kurang terartikulasi dengan baik
- Kelemahan format dan presentasi

## Format Output yang Diperlukan:

**📊 SKOR KESESUAIAN: [X/10]**
*Penjelasan singkat rationale scoring*

**✅ KEKUATAN UTAMA:**
- [Requirement spesifik] → [Bukti konkret dari CV dengan hasil terukur]
- [Sertakan 3-5 keselarasan terkuat dengan contoh konkret]

**🎯 INVENTARIS KEMAMPUAN:**
- **Skill Teknis yang Ditemukan:** [List dengan bukti kemampuan]
- **Soft Skills yang Terdemonstrasikan:** [Dengan contoh spesifik]
- **Skill yang Hilang tapi Dibutuhkan:** [Dari job description]
- **Skill Tersembunyi untuk Ditonjolkan:** [Kekuatan yang kurang dimanfaatkan]

**💼 EVALUASI PENGALAMAN:**
- **Pengalaman Relevan:** [Bagaimana setiap peran terhubung dengan target job]
- **Kuantifikasi Pencapaian:** [Saat ini vs. rekomendasi metrik]
- **Cerita Progres Karir:** [Penilaian koherensi narasi]

**🔧 PRIORITAS PERBAIKAN:**
1. **Perbaikan Cepat (24-48 jam):**
   - [Quick wins seperti optimasi keyword, formatting]
2. **Peningkatan Konten (1-2 minggu):**
   - [Menulis ulang bagian, menambah achievement, demonstrasi skill]
3. **Penambahan Strategis (1 bulan+):**
   - [Sertifikasi yang perlu dikejar, pengalaman yang perlu didapat, skill yang perlu dikembangkan]

**💡 REKOMENDASI SPESIFIK:**

**Format & Struktur:**
- [Saran formatting spesifik]
- [Advice reorganisasi section]
- [Optimasi panjang dan layout]

**Peningkatan Konten:**
- [Perbaikan wording eksak dengan contoh before/after sesuaikan dengan bahasa yang digunakan di cv]
- [Saran kuantifikasi achievement]
- [Integrasi bahasa spesifik industri]

**Optimasi Kata Kunci:**
- **Kata Kunci Wajib Ditambah:** [List dari job description]
- **Saran Integrasi Natural:** [Cara mengintegrasikan secara autentik]

---

## Panduan Tambahan:
- Berikan advice yang spesifik dan implementable, bukan saran generik
- Sertakan actual phrase/sentence improvement jika memungkinkan
- Pertimbangkan praktik hiring Indonesia dan budaya kerja lokal
- Address kebutuhan human recruiter dan algoritma ATS
- Maintain tone yang encouraging dan konstruktif sepanjang feedback
- Gunakan bahasa yang familiar dengan konteks kerja Indonesia
- Pertimbangkan ekspektasi salary dan benefit yang realistis untuk pasar Indonesia
"""

    async def analyze_resume(self, resume_content: str, job_description: str) -> Dict[str, Any]:
        try:
            prompt = self.analysis_prompt_template.format(
                job_description=job_description,
                resume_content=resume_content
            )
            response = await asyncio.to_thread(
                self.model.generate_content,
                prompt
            )
            analysis_text = response.text
            score = self._extract_score(analysis_text)
            return {
                'score': score,
                'analysis': analysis_text,
                'status': 'success'
            }
        except Exception as e:
            logging.error(f"Error analyzing resume: {e}")
            return {
                'score': 0,
                'analysis': f'Error analyzing resume: {str(e)}',
                'status': 'error'
            }
    def _extract_score(self, analysis_text: str) -> int:
        """Extract numerical score from analysis text"""
        import re
        try:
            # Cari pola "SKOR KESESUAIAN: 7/10" atau "Score: 7/10"
            match = re.search(r'(SKOR KESESUAIAN|Score)[^\d]*(\d+)\s*/\s*10', analysis_text, re.IGNORECASE)
            if match:
                return int(match.group(2))
            # fallback: cari angka setelah "SKOR KESESUAIAN" atau "Score"
            match = re.search(r'(SKOR KESESUAIAN|Score)[^\d]*(\d+)', analysis_text, re.IGNORECASE)
            if match:
                return int(match.group(2))
            return 0
        except Exception as e:
            logging.error(f"Score extraction error: {e}")
            return 0

class ResultRenderer:
    """Handle HTML rendering of results"""

    @staticmethod
    def render_results(analyses: List[Dict[str, Any]], job_description: str) -> str:
        """Render analysis results as HTML"""
        #short by score (highest first)
        sorted_analyses = sorted(analyses, key=lambda x: x['score'], reverse=True)

        html_result = "<div class='results-container'>"
        html_result += "<h3 class='mb-4'>📊 Candidate Rankings</h3>"

        for idx, analysis in enumerate(sorted_analyses, 1):
            score = analysis['score']
            status = analysis['status']

            #determine color based on score
            badge_class = "success" if score >= 8 else "warning" if score >= 6 else 'danger'


            html_result += f"""
            <div class="card mb-3">
                <div class="card-header d-flex justify-content-between align-items-center">
                    <h5 class="mb-0">🎯 Candidate #{idx}</h5>
                    <span class="badge bg-{badge_class} fs-6">Score: {score}/10</span>
                </div>
                <div class="card-body">
            """

            if status == 'success':
                #convert markdown to HTML
                analysis_html = markdown.markdown(analysis['analysis'])
                html_result += analysis_html
            else:
                html_result += f"<div class='alert alert-danger'>{analysis['analysis']}</div>"
            
            html_result +=  "</div></div>"
        
        html_result += "</div>"
        html_result += "<div class='mt-4'><a href='/' class='btn btn-primary'>🔄 Analyze More Resumes</a></div>"
        
        return html_result

    def _create_results_page(self, html_results: str, job_description: str, file_count: int) ->str:
        """Create complete results page HTML"""
        with open("templates/results.html", "r", encoding="utf-8") as f:
            template = f.read()


        #replace placeholders
        template = template.replace("{{RESULTS_CONTENT}}", html_results)  
        template = template.replace("{{JOB_DESCRIPTION}}", job_description[:500] + ('...' if len(job_description) > 500 else ''))
        template = template.replace("{{FILE_COUNT}}", str(file_count))

        return template

#Initialize components
doc_processor = DocumentProcessor()
resume_analyzer = ResumeAnalyzer()
result_renderer = ResultRenderer()

@app.get("/", response_class=HTMLResponse)
async def upload_form():
    """Serve the main upload form"""
    with open("templates/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.post("/analyze/")
async def analyze_resumes_endpoint(
    files: List[UploadFile] = File(...),
    prompt: str = Form(...)
):
    task_id = str(uuid.uuid4())
    logging.info(f"starting resume analysis task {task_id} with {len(files)}files") 
    
    if not GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="Gemini API key not configured")

    try:
        #process each uploade file
        analyses = []

        for idx, file in enumerate(files):
            logging.info(f"Processing file {idx+1}/{len(files)}: {file.filename}")

            #read file content
            file_content = await file.read()

            #Extract text from file
            try:
                resume_text = doc_processor.process_file(file_content, file.filename)

                if not resume_text.strip():
                    analyses.append({
                        'score': 0,
                        'analysis': f'**Error**: Could not extract text from {file.filename}',
                        'status': 'error'
                    })
                    continue

                #analyze resume
                analysis = await resume_analyzer.analyze_resume(resume_text, prompt)
                analyses.append(analysis)

            except ValueError as e:
                analyses.append({
                    'score': 0,
                    'analysis': f'**Error**: {str(e)} for file {file.filename}',
                    'status': 'error'
                })
            except Exception as e:
                logging.error(f"Unexpected error processing {file.filename}: {e}")
                analyses.append({
                    'score': 0,
                    'analysis': f'**Error**: Unexpected error processing {file.filename}',
                    'status': 'error'
                })
        
        #render results
        html_results = result_renderer.render_results(analyses, prompt)
        
        #create results html file
        results_html = result_renderer._create_results_page(html_results, prompt, len(files))

        return HTMLResponse(content=results_html)
    
    except Exception as e:
        logging.error(f"Error during analysis: {e}")

        #create error page
        error_html = self._create_error_page(str(e))

        return HTMLResponse(content=error_html, status_code=500)
    
def _create_error_page(error_message: str) -> str:
    """Create error page HTML"""
    with open("templates/error.html", "r", encoding="utf-8") as f:
        template = f.read()

    #replace placeholders
    template = template.replace("{{ERROR_MESSAGE}}", error_message)

    return template

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "model": GEMINI_MODEL}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Export app untuk Vercel
handler = app
