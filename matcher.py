from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_similarity(resume_text, job_description):

    documents = [
        resume_text,
        job_description
    ]

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    vectors = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(
        vectors[0:1],
        vectors[1:2]
    )[0][0]

    return round(similarity * 100, 2)


def calculate_skill_score(
    resume_skills,
    job_skills
):

    if len(job_skills) == 0:

        return 0

    resume_set = set(resume_skills)

    job_set = set(job_skills)

    matched = resume_set.intersection(job_set)

    score = (
        len(matched) /
        len(job_set)
    ) * 100

    return round(score, 2)


def get_matched_skills(
    resume_skills,
    job_skills
):

    resume_set = set(resume_skills)

    job_set = set(job_skills)

    return sorted(
        list(
            resume_set.intersection(
                job_set
            )
        )
    )


def get_missing_skills(
    resume_skills,
    job_skills
):

    resume_set = set(resume_skills)

    job_set = set(job_skills)

    return sorted(
        list(
            job_set - resume_set
        )
    )


def calculate_final_score(
    similarity_score,
    skill_score
):

    final_score = (
        similarity_score * 0.40
        +
        skill_score * 0.60
    )

    return round(final_score, 2)


def get_recommendation(score):

    if score >= 80:

        return (
            "Excellent match! "
            "Your resume is highly suitable "
            "for this job."
        )

    elif score >= 60:

        return (
            "Good match! "
            "Improve the missing skills "
            "to increase your chances."
        )

    elif score >= 40:

        return (
            "Average match. "
            "You should improve your technical "
            "skills and resume."
        )

    else:

        return (
            "Low match. "
            "Try learning the required skills "
            "and update your resume."
        )