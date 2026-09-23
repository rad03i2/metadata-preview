import hashlib
from pathlib import Path

import pytest
from PIL import Image
from pypdf import PdfWriter

from metadata_preview.core import inspect_file


def test_plain_file_and_hash(tmp_path: Path):
    path = tmp_path / "مرحبا.txt"
    path.write_text("hello metadata", encoding="utf-8")
    report = inspect_file(path, include_hash=True)
    assert report["name"] == "مرحبا.txt"
    assert report["size_bytes"] == len(b"hello metadata")
    assert report["sha256"] == hashlib.sha256(b"hello metadata").hexdigest()
    assert report["mime_type"].startswith("text/")


def test_image_dimensions(tmp_path: Path):
    path = tmp_path / "photo.png"
    Image.new("RGB", (13, 7)).save(path)
    report = inspect_file(path)
    assert report["image"]["width"] == 13
    assert report["image"]["height"] == 7
    assert report["image"]["format"] == "PNG"


def test_pdf_page_count_and_metadata(tmp_path: Path):
    path = tmp_path / "doc.pdf"
    writer = PdfWriter()
    writer.add_blank_page(width=100, height=100)
    writer.add_metadata({"/Title": "Test title"})
    with path.open("wb") as stream:
        writer.write(stream)
    report = inspect_file(path)
    assert report["pdf"]["pages"] == 1
    assert report["pdf"]["document_info"]["Title"] == "Test title"


def test_missing_file_rejected(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        inspect_file(tmp_path / "missing.txt")


def test_directory_rejected(tmp_path: Path):
    with pytest.raises(ValueError):
        inspect_file(tmp_path)
