import os
import requests
import streamlit as st

# Fetch the OpenAI API key from an environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    st.error("OpenAI API key is not set. Please set the OPENAI_API_KEY environment variable.")
    st.stop()

st.title('🎨 Art Critique')

def analyze_artwork(image_url):
    """
    Sends an image URL to the OpenAI API's gpt-4-vision-preview model for analysis,
    providing a critique in the style of a professional art critic. Includes potential
    artwork identification with responsible caveats.
    """
    try:
        json_data = {
            "model": "gpt-4-vision-preview",
            "messages": [
                {
                    "role": "assistant",
                    "content": [
                        {"type": "text", "text": "Assuming this artwork is well-known, identify the artwork's title and artist, if possible."},
                        {"type": "text", "text": "Describe the image in detail, focusing on style, colors, shapes, composition, and the overall scene."},
                        {"type": "text", "text": "Analyze the artist's use of color, brushstrokes (if visible), and perspective. Comment on the artwork's technical proficiency."},
                        {"type": "text", "text": "Discuss the composition and its effectiveness. Does the artwork adhere to a particular artistic style or movement? Explain."},
                        {"type": "text", "text": "Describe the mood the artwork evokes, and explain how visual elements contribute to it. Does the artwork have potential symbolism or deeper meaning?"},
                        {"type": "image_url", "image_url": image_url}
                    ]
                }
            ],
            "max_tokens": 500
        }

        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {openai_api_key}"},
            json=json_data
        )

        response.raise_for_status()
        data = response.json()

        if data['choices']:
            result = data['choices'][0]['message']['content']
            st.markdown("### Art Critique")
            st.write(result)
        else:
            st.write("No response generated or invalid response structure.")

    except Exception as e:
        st.write(f"Error processing your request: {str(e)}")

# User inputs
image_url = st.text_input("Paste the image URL here:")

if st.button('Get Art Critique'):
    if image_url:
        st.image(image_url, caption='Uploaded Artwork')
        with st.spinner('Generating critique...'):
            analyze_artwork(image_url)
    else:
        st.error("Please enter a valid image URL.")























