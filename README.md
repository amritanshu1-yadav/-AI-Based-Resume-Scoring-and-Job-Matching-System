# AI-Based Resume Scoring and Job Matching System

## About the Project

A web-based system that compares a PDF resume with a job description and calculates a resume-job matching score.

## Features

- PDF resume upload
- Resume text extraction
- Skill extraction
- Text similarity
- Skill matching
- Matched skills
- Missing skills
- Overall match score
- Recommendation
- Analysis history
- Clear history

## Technologies

- Python
- Flask
- HTML
- CSS
- SQLite
- Text Similarity
- PDF Text Extraction

## Project Structure

AI-Resume-Scoring-Job-Matching-System/
├── app.py
├── matcher.py
├── resume_parser.py
├── database.py
├── templates/
├── static/
├── requirements.txt
└── README.md

## How to Run

1. Clone the repository.
2. Install the required packages.
3. Run the Flask application.
4. Open the local URL in a browser.

```bash
pip install -r requirements.txt
python app.py