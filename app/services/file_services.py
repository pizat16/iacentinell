import os, aiofiles
from datetime import datetime
from app.services.hash_service import sha256_bytes

UPLOAD_DIR = "app/uploads"

async def save_upload(file_bytes: bytes, filename: str) -> dict:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    safe_name = f"{ts}_{filename}"
    path = os.path.join(UPLOAD_DIR, safe_name)
    async with aiofiles.open(path, "wb") as f:
        await f.write(file_bytes)
    return {"original_name": filename, "saved_name": safe_name,
            "path": path, "size": len(file_bytes),
            "sha256": sha256_bytes(file_bytes)}

def get_mime_type(file_bytes: bytes, filename: str) -> str:
    try:
        import magic
        return magic.from_buffer(file_bytes, mime=True)
    except Exception:
        ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else "unknown"
        return {"exe":"application/x-dosexec","pdf":"application/pdf",
                "zip":"application/zip","py":"text/x-python",
                "js":"application/javascript","txt":"text/plain"
                }.get(ext, "application/octet-stream")
