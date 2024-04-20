import streamlit as st
import openai
import os

# OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")

# Check if the API key is set
if not api_key:
    st.error("OpenAI API key is not set. Please set the OPENAI_API_KEY environment variable.")
    st.stop()

client = openai.OpenAI(api_key=api_key)


def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0
    )
    return response.choices[0].message.content


# Analyzer UI
st.title('Elevate Your Job Search: Resume Analyzer 🔎📄')
st.markdown(
    'Optimize your resume for specific job descriptions. Get tailored insights into your skills, experience, and education alignment')


def compare_resume_to_job_description(resume_text, job_description_text):
    # Frame the prompt for resume and job description comparison
    prompt = f"Given a resume with the following details:\n{resume_text}\n\nAnd a job description as follows:\n{job_description_text}\n\nPlease analyze and compare the skill sets, qualifications, and experiences. Provide an estimate of the qualification match as a percentage."

    # Use get_completion function to get the AI response
    result = get_completion(prompt)

    return result


resume_text = st.text_area("Paste your resume here:", height=300)
job_description_text = st.text_area("Paste the job description here:", height=300)

if st.button('Analyze Resume'):
    with st.spinner('Your resume is under the microscope...'):
        result = compare_resume_to_job_description(resume_text, job_description_text)
        if result:
            st.write(result)
