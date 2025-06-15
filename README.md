# Document Fraud Detector

This project is an API built with FastAPI that detects and extracts text from images and PDF documents to support potential document fraud detection. It uses OCR (Optical Character Recognition) via Tesseract and can process both images and scanned PDFs.

## Features

- Upload and process `.jpg`, `.jpeg`, `.png` images and `.pdf` documents
- Extracts text using Tesseract OCR
- API developed with FastAPI
- Simple file upload endpoint for testing

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/cdiazcastilla/doc-fraud-detector.git
cd doc-fraud-detector

2. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate

3. Install dependencies
pip install -r requirements.txt

4. Install Tesseract OCR
Download and install Tesseract OCR from:

https://github.com/tesseract-ocr/tesseract

Make sure to update the pytesseract.pytesseract.tesseract_cmd path in app/main.py to match your local installation.

5. Start the server
uvicorn app.main:app --reload
Visit http://127.0.0.1:8000/docs to test the API.

API Endpoints
GET / — Root endpoint

POST /upload/ — Upload and process image or PDF

Future Improvements
Add fraud detection logic based on text anomalies or metadata

Integrate with machine learning models for classification

Include database logging and audit trail

Thanks for visiting this repository.
If you have any feedback or suggestions, feel free to open an issue or reach out.

Warm regards,
Carlos Díaz

