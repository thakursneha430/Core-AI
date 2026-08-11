from pathlib import Path

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from src.pipeline.document_pipeline import DocumentPipeline
from src.rag.rag_pipeline import RAGPipeline

app = FastAPI(
    title="Multimodal Document Intelligence API",
    version="1.0.0"
)

# ==========================================
# CORS Configuration
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:8000",
        "http://localhost:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# Paths
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

FRONTEND_DIR = BASE_DIR / "frontend"

UPLOAD_DIR = BASE_DIR / "data" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# ==========================================
# Serve Frontend
# ==========================================

if (FRONTEND_DIR / "css").exists():
    app.mount(
        "/css",
        StaticFiles(directory=FRONTEND_DIR / "css"),
        name="css"
    )

if (FRONTEND_DIR / "js").exists():
    app.mount(
        "/js",
        StaticFiles(directory=FRONTEND_DIR / "js"),
        name="js"
    )

if (FRONTEND_DIR / "assets").exists():
    app.mount(
        "/assets",
        StaticFiles(directory=FRONTEND_DIR / "assets"),
        name="assets"
    )

# ==========================================
# Initialize Pipelines
# ==========================================

document_pipeline = DocumentPipeline()
rag_pipeline = RAGPipeline()

# ==========================================
# Request Model
# ==========================================

class QuestionRequest(BaseModel):
    question: str

# ==========================================
# Home Page
# ==========================================

@app.get("/", include_in_schema=False)
async def home():

    index_file = FRONTEND_DIR / "index.html"

    if index_file.exists():
        return FileResponse(index_file)

    return {
        "message": "Frontend not found.",
        "frontend_path": str(index_file)
    }

# ==========================================
# Health Check
# ==========================================

@app.get("/health")
def health():
    return {"status": "healthy"}

# ==========================================
# Upload API
# ==========================================

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    try:

        file_path = UPLOAD_DIR / file.filename

        with open(file_path, "wb") as f:
            f.write(await file.read())

        result = document_pipeline.process(str(file_path))

        return {
            "message": "Document indexed successfully.",
            "filename": file.filename,
            "stored_chunks": result["stored_chunks"]
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

# ==========================================
# Ask API
# ==========================================

@app.post("/ask")
async def ask_question(request: QuestionRequest):
    try:

        result = rag_pipeline.ask(request.question)

        return {
            "question": result["question"],
            "answer": result["answer"],
            "sources": result["sources"]
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )