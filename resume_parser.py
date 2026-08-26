from pypdf import PdfReader


SKILLS = [

    "python",
    "java",
    "c",
    "c++",

    "html",
    "css",
    "javascript",

    "react",
    "node.js",
    "express",

    "sql",
    "mysql",
    "mongodb",

    "git",
    "github",

    "machine learning",
    "deep learning",

    "data science",

    "pandas",
    "numpy",

    "tensorflow",
    "keras",

    "flask",
    "django",

    "php",
    "bootstrap",

    "android",
    "kotlin",

    "aws",
    "azure"
]


def extract_text_from_pdf(file):

    reader = PdfReader(file)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:

            text += page_text + "\n"

    return text


def extract_skills(text):

    text = text.lower()

    found_skills = []

    for skill in SKILLS:

        if skill.lower() in text:

            found_skills.append(skill)

    return found_skills