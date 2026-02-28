import uuid
from pathlib import Path
from fastapi import UploadFile, HTTPException


UPLOAD_DIR = Path("uploads")
DOC_DIR = UPLOAD_DIR / "documents"
CHEQUE_DIR = UPLOAD_DIR / "cheques"

DOC_DIR.mkdir(parents=True, exist_ok=True)
CHEQUE_DIR.mkdir(parents=True, exist_ok=True)

DOC_MAX = 5 * 1024 * 1024
CHEQUE_MAX = 3 * 1024 * 1024


async def save_file(file: UploadFile, target_dir: Path, max_size: int):
    content = await file.read()

    if len(content) > max_size:
        raise HTTPException(status_code=400, detail="File too large")

    ext = Path(file.filename).suffix
    filename = f"{uuid.uuid4().hex}{ext}"
    file_path = target_dir / filename

    file_path.write_bytes(content)

    return str(file_path)