from __future__ import annotations

import hashlib
import mimetypes
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from PIL import ExifTags, Image, UnidentifiedImageError
from pypdf import PdfReader

_IMAGE_EXTS = {".jpg", ".jpeg", ".tif", ".tiff", ".png", ".webp"}


def _iso(ts: float) -> str:
    return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()


def _json_safe(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, bytes):
        return f"<bytes:{len(value)}>"
    if isinstance(value, (list, tuple)):
        return [_json_safe(v) for v in value]
    if isinstance(value, dict):
        return {str(k): _json_safe(v) for k, v in value.items()}
    return str(value)


def sha256(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()


def _image_metadata(path: Path) -> dict[str, Any]:
    try:
        with Image.open(path) as image:
            result: dict[str, Any] = {
                "format": image.format,
                "width": image.width,
                "height": image.height,
                "mode": image.mode,
            }
            exif = image.getexif()
            if exif:
                result["exif"] = {
                    ExifTags.TAGS.get(tag, str(tag)): _json_safe(value)
                    for tag, value in exif.items()
                }
            return result
    except (UnidentifiedImageError, OSError) as exc:
        return {"error": f"Unable to read image metadata: {exc}"}


def _pdf_metadata(path: Path) -> dict[str, Any]:
    try:
        reader = PdfReader(str(path))
        metadata = reader.metadata or {}
        return {
            "pages": len(reader.pages),
            "document_info": {str(k).lstrip("/"): _json_safe(v) for k, v in metadata.items()},
            "encrypted": bool(reader.is_encrypted),
        }
    except Exception as exc:  # pypdf exposes multiple parser exceptions across versions
        return {"error": f"Unable to read PDF metadata: {exc}"}


def inspect_file(path: str | Path, *, include_hash: bool = False) -> dict[str, Any]:
    source = Path(path).expanduser()
    if not source.exists():
        raise FileNotFoundError(f"File does not exist: {source}")
    if source.is_symlink():
        raise ValueError("Symbolic links are not inspected")
    if not source.is_file():
        raise ValueError(f"Not a regular file: {source}")

    stat = source.stat()
    result: dict[str, Any] = {
        "path": str(source.resolve()),
        "name": source.name,
        "extension": source.suffix.lower(),
        "mime_type": mimetypes.guess_type(source.name)[0] or "application/octet-stream",
        "size_bytes": stat.st_size,
        "modified_utc": _iso(stat.st_mtime),
        "created_utc": _iso(stat.st_ctime),
    }
    if include_hash:
        result["sha256"] = sha256(source)
    suffix = source.suffix.lower()
    if suffix in _IMAGE_EXTS:
        result["image"] = _image_metadata(source)
    elif suffix == ".pdf":
        result["pdf"] = _pdf_metadata(source)
    return result


def inspect_many(paths: Iterable[str | Path], *, include_hash: bool = False) -> list[dict[str, Any]]:
    return [inspect_file(path, include_hash=include_hash) for path in paths]
