import streamlit as st
from openai import OpenAI
import os

# OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")

# Check if the API key is set
if not api_key:
    st.error("OpenAI API key is not set. Please set the OPENAI_API_KEY environment variable.")
    st.stop()

client = OpenAI(api_key=api_key)

# Analyzer UI
st.title('Elevate Your Job Search: Resume Analyzer 🔎📄')
st.markdown('Optimize your resume for specific job descriptions. Get tailored insights into your skills, experience, and education alignment')

# Start OPENAI API
def compare_resume_to_job_description(resume_text, job_description_text):
    client = OpenAI(api_key=api_key)
    model = "gpt-3.5-turbo"

    # Instructions for the AI
    messages = [
        {"role": "system",
         "content": "You are an assistant who helps individuals identify gaps in their resumes based on job descriptions."},
        {"role": "user",
         "content": f"Compare the resume and the job description. Identify skill gaps and estimate how qualified the individual is for the job. Provide a detailed analysis including the qualification percentage.\n{resume_text, job_description_text}"}
    ]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0
    )
    return response.choices[0].message.content

resume_text = st.text_area("Paste your resume here:", height=300)
job_description_text = st.text_area("Paste the job description here:", height=300)

if st.button('Analyze Resume'):
    with st.spinner('Your resume is under the microscope...'):
        result = compare_resume_to_job_description(resume_text, job_description_text)
        if result:
            st.write(result)
