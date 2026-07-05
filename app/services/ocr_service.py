import os
import re
from pathlib import Path

from app.models import Medicine


PRINTED_ONLY_NOTICE = "This OCR currently supports printed prescriptions only. Handwritten prescriptions may not be recognised accurately."
DEFAULT_TESSERACT_CMD = os.environ.get("TESSERACT_CMD", "tesseract")


def extract_prescription_text(file_storage):
    if not file_storage:
        return _mock_text(), "mock"
    try:
        import pytesseract
        from PIL import Image

        if DEFAULT_TESSERACT_CMD == "tesseract" or Path(DEFAULT_TESSERACT_CMD).exists():
            pytesseract.pytesseract.tesseract_cmd = DEFAULT_TESSERACT_CMD
        image = Image.open(file_storage.stream)
        text = pytesseract.image_to_string(image)
        return text.strip() or _mock_text(), "tesseract"
    except Exception:
        return _mock_text(), "mock"


def recognize_medicines(text):
    matches = []
    unmatched = []
    lines = [line.strip() for line in re.split(r"[\n;]", text) if line.strip()]
    for line in lines:
        medicine = _match_medicine(line)
        quantity = _extract_quantity(line)
        dosage = _extract_dosage(line)
        if medicine:
            matches.append(
                {
                    "medicine": medicine,
                    "source_text": line,
                    "quantity": quantity,
                    "dosage": dosage,
                    "confidence": 92 if medicine.name.split()[0].lower() in line.lower() else 78,
                }
            )
        else:
            unmatched.append({"source_text": line, "confidence": 32})
    return matches, unmatched


def _match_medicine(text):
    token = text.split()[0] if text.split() else ""
    if not token:
        return None
    return Medicine.query.filter(Medicine.name.ilike(f"%{token}%")).first()


def _extract_quantity(text):
    match = re.search(r"(\d+)\s*(tablet|capsule|strip|sheet|box|bottle|ml)?", text, re.I)
    if not match:
        return 1
    return max(1, int(match.group(1)))


def _extract_dosage(text):
    match = re.search(r"(\d+\s?(?:mg|ml|iu|mcg))", text, re.I)
    return match.group(1) if match else "Dose needs review"


def _mock_text():
    return "Metformin 500 mg 2 strips after breakfast; Amlodipine 5 mg 1 strip after dinner; Vitamin note handwritten"
