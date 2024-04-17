import streamlit as st
import requests

# Your OpenAI API key
openai_api_key = ""

st.title('🎨 AI Art Critique Assistant')
st.markdown('Upload an image URL and provide a detailed description of the artwork for analysis.')


def generate_artwork_critique(description):
    """
    Sends a description of artwork to the OpenAI API using the GPT-3.5 Turbo model,
    requesting not just a critique but also explanations of any specific art techniques mentioned.
    """
    # Enhanced prompt to request technique explanations within the critique
    prompt = f"Provide a detailed critique of the artwork described below, and include explanations " \
             f"of any specific art techniques used:\n{description}"

    headers = {
        "Authorization": f"Bearer {openai_api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are an AI trained to critique artwork and explain art techniques."},
            {"role": "user", "content": prompt}
        ]
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return "Failed to generate critique."


# User inputs
image_url = st.text_input("Paste the image URL here:")
description_input = st.text_area("Enter the name of the artwork:")

# Generate and display critique with integrated art technique explanations
if st.button('Generate Art Critique'):
    if image_url:
        st.image(image_url, caption='Uploaded Artwork')
        if description_input:
            with st.spinner('Generating critique...'):
                result = generate_artwork_critique(description_input)
                st.markdown("### Generated Art Critique with Art Technique Explanations")
                st.write(result)
        else:
            st.error("Please provide a description to generate a critique.")
    else:
        st.error("Please enter a valid image URL.")
