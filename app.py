import streamlit as st
import os
from groq import Groq

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

st.set_page_config(page_title="AI Interview Assistant")

st.title("🎯 AI Interview Preparation Assistant")

jd = st.text_area(
    "Paste Job Description",
    height=200
)

if st.button("Generate Interview Questions"):

    prompt = f"""
    You are an expert interviewer.

    Analyze the following job description and generate:

    - 3 Technical Questions
    - 2 Behavioral Questions

    Job Description:
    {jd}

    Return only numbered questions.
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    questions = response.choices[0].message.content

    st.session_state.questions = questions

if "questions" in st.session_state:

    st.subheader("Generated Questions")

    st.write(st.session_state.questions)

    st.subheader("Your Answers")

    answers = st.text_area(
        "Answer all questions here",
        height=250
    )

    if st.button("Evaluate Answers"):

        evaluation_prompt = f"""
        You are a professional interview evaluator.

        Interview Questions:
        {st.session_state.questions}

        Candidate Answers:
        {answers}

        Evaluate:

        1. Technical Knowledge (Score /10)
        2. Communication (Score /10)
        3. Problem Solving (Score /10)

        Provide:
        - Overall Score
        - Strengths
        - Weaknesses
        - Improvement Suggestions
        - Interview Readiness Assessment
        """

        evaluation = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": evaluation_prompt}
            ]
        )

        result = evaluation.choices[0].message.content

        st.subheader("AI Feedback")

        st.write(result)