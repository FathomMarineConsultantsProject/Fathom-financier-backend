import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "")

UPLOAD_ROOT = Path("uploads")
DOC_DIR = UPLOAD_ROOT / "documents"
CHEQUE_DIR = UPLOAD_ROOT / "cheques"

DOC_MAX = 5 * 1024 * 1024      # 5MB
CHEQUE_MAX = 3 * 1024 * 1024   # 3MB

DOC_TYPES = {
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}

CHEQUE_TYPES = {"image/jpeg", "image/png", "image/webp"}

def ensure_upload_dirs():
    DOC_DIR.mkdir(parents=True, exist_ok=True)
    CHEQUE_DIR.mkdir(parents=True, exist_ok=True)