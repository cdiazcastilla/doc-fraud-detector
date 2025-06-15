from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import pytesseract
import cv2
import numpy as np
import fitz  # PyMuPDF
from pdf2image import convert_from_bytes
import re
import os

# Ruta de Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Ruta de Poppler para Windows
POPPLER_PATH = r"C:\ruta\a\poppler\bin"  # <- Cambia esto a tu ruta real

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Document Fraud Detector API"}

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    text_total = ""

    if file.filename.lower().endswith((".png", ".jpg", ".jpeg")):
        # Procesar imagen
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        text_total = pytesseract.image_to_string(img)

    elif file.filename.lower().endswith(".pdf"):
        # Procesar PDF con texto
        with fitz.open(stream=contents, filetype="pdf") as doc:
            for page in doc:
                text_total += page.get_text()

        # Si no hay texto, usar OCR sobre imágenes
        if text_total.strip() == "":
            images = convert_from_bytes(contents, poppler_path=POPPLER_PATH)
            for image in images:
                img_cv = np.array(image)
                text_total += pytesseract.image_to_string(img_cv)

    else:
        return {"filename": file.filename, "message": "Formato no compatible"}

    # === Reglas de fraude ===
    sospechoso = False
    motivos = []

    # 1. Texto demasiado corto
    if len(text_total.strip()) < 100:
        sospechoso = True
        motivos.append("Texto demasiado corto para un documento oficial")

    # 2. Palabras clave faltantes
    palabras_clave = ["REPUBLICA", "CEDULA", "CIUDADANIA"]
    for palabra in palabras_clave:
        if palabra not in text_total.upper():
            sospechoso = True
            motivos.append(f"Falta la palabra clave: {palabra}")

    # 3. Formato de cédula ausente
    if not re.search(r"\d{2}[.,]?\d{3}[.,]?\d{3}", text_total):
        sospechoso = True
        motivos.append("No se detectó un número de cédula con el formato esperado")

    # Respuesta
    return {
        "filename": file.filename,
        "type": "image" if file.filename.lower().endswith((".png", ".jpg", ".jpeg")) else "pdf",
        "text": text_total.strip(),
        "sospechoso": sospechoso,
        "motivos": motivos
    }
