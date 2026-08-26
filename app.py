from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for
)

import os
import sqlite3

from resume_parser import (
    extract_text_from_pdf,
    extract_skills
)

from matcher import (
    calculate_similarity,
    calculate_skill_score,
    get_matched_skills,
    get_missing_skills,
    calculate_final_score,
    get_recommendation
)

from database import (
    create_database,
    save_analysis,
    get_history
)


# =========================================================
# FLASK APP
# =========================================================

app = Flask(__name__)


# =========================================================
# UPLOAD FOLDER
# =========================================================

UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


# =========================================================
# CREATE DATABASE
# =========================================================

create_database()


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# =========================================================
# ANALYZE RESUME
# =========================================================

@app.route(
    "/analyze",
    methods=["POST"]
)
def analyze():

    # -----------------------------------------------------
    # Get uploaded resume
    # -----------------------------------------------------

    resume = request.files.get(
        "resume"
    )


    # -----------------------------------------------------
    # Get job information
    # -----------------------------------------------------

    job_title = request.form.get(
        "job_title",
        "Unknown Job"
    )

    job_description = request.form.get(
        "job_description",
        ""
    )


    # -----------------------------------------------------
    # Validate resume
    # -----------------------------------------------------

    if not resume:

        return "Please upload a resume."


    if resume.filename == "":

        return "Please select a PDF file."


    if not resume.filename.lower().endswith(
        ".pdf"
    ):

        return "Only PDF files are allowed."


    # -----------------------------------------------------
    # Validate job description
    # -----------------------------------------------------

    if not job_description.strip():

        return "Please enter job description."


    # =====================================================
    # SAVE RESUME
    # =====================================================

    file_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        resume.filename
    )

    resume.save(
        file_path
    )


    # =====================================================
    # EXTRACT TEXT FROM PDF
    # =====================================================

    try:

        resume_text = extract_text_from_pdf(
            file_path
        )

    except Exception as error:

        return (
            "Could not read PDF: "
            + str(error)
        )


    # -----------------------------------------------------
    # Check extracted text
    # -----------------------------------------------------

    if not resume_text.strip():

        return (
            "No readable text found "
            "in this PDF."
        )


    # =====================================================
    # EXTRACT SKILLS
    # =====================================================

    resume_skills = extract_skills(
        resume_text
    )

    job_skills = extract_skills(
        job_description
    )


    # =====================================================
    # CALCULATE TEXT SIMILARITY
    # =====================================================

    similarity_score = calculate_similarity(
        resume_text,
        job_description
    )


    # =====================================================
    # CALCULATE SKILL SCORE
    # =====================================================

    skill_score = calculate_skill_score(
        resume_skills,
        job_skills
    )


    # =====================================================
    # GET MATCHED SKILLS
    # =====================================================

    matched_skills = get_matched_skills(
        resume_skills,
        job_skills
    )


    # =====================================================
    # GET MISSING SKILLS
    # =====================================================

    missing_skills = get_missing_skills(
        resume_skills,
        job_skills
    )


    # =====================================================
    # CALCULATE FINAL SCORE
    # =====================================================

    final_score = calculate_final_score(
        similarity_score,
        skill_score
    )


    # =====================================================
    # GET RECOMMENDATION
    # =====================================================

    recommendation = get_recommendation(
        final_score
    )


    # =====================================================
    # SAVE ANALYSIS TO DATABASE
    # =====================================================

    save_analysis(

        resume.filename,

        job_title,

        final_score,

        skill_score,

        similarity_score,

        ", ".join(
            matched_skills
        ),

        ", ".join(
            missing_skills
        )
    )


    # =====================================================
    # RESULT DATA
    # =====================================================

    result = {

        "resume_name":
            resume.filename,

        "job_title":
            job_title,

        "score":
            final_score,

        "skill_score":
            skill_score,

        "similarity_score":
            similarity_score,

        "resume_skills":
            resume_skills,

        "job_skills":
            job_skills,

        "matched_skills":
            matched_skills,

        "missing_skills":
            missing_skills,

        "recommendation":
            recommendation
    }


    # =====================================================
    # RESULT PAGE
    # =====================================================

    return render_template(
        "result.html",
        result=result
    )


# =========================================================
# HISTORY PAGE
# =========================================================

@app.route("/history")
def history():

    data = get_history()

    return render_template(
        "history.html",
        history=data
    )


# =========================================================
# CLEAR HISTORY
# =========================================================

@app.route(
    "/clear-history",
    methods=["POST"]
)
def clear_history():

    connection = sqlite3.connect(
        "resume_matcher.db"
    )

    cursor = connection.cursor()


    # Delete all analysis records

    cursor.execute(
        "DELETE FROM analyses"
    )


    # Reset ID counter

    cursor.execute(
        "DELETE FROM sqlite_sequence "
        "WHERE name='analyses'"
    )


    connection.commit()

    connection.close()


    # Go back to history page

    return redirect(
        "/history"
    )


# =========================================================
# RUN FLASK APPLICATION
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )