import streamlit as st
import os
import openai

# Set the API key for OpenAI from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

# Validate that the API key is available
if not openai.api_key:
    st.error("OPENAI_API_KEY environment variable not set")
    st.stop()

# Designing the UI Layout
st.title('Merch AI Designer: Revolutionizing Merchandise Creation')
st.sidebar.header("Design Customization")

# User Inputs
description_input = st.sidebar.text_input("Describe your merch design:", "")
merch_type = st.sidebar.selectbox("Select Merchandise Type:",
                                  ['T-Shirt', 'Mug', 'Poster', 'Tote Bag',
                                   'Phone Case', 'Sticker', 'Pillow', 'Hoodie'])

# Submit Button
submit_button = st.sidebar.button('Generate Design')

# Processing User Inputs
if submit_button:
    try:
        # Generate Image using OpenAI API
        response = openai.images.generate(
            model="dall-e-3",
            prompt=description_input + " design on a " + merch_type,
            size="1024x1024",
            quality="hd",
            n=1
        )

        # Check response structure and handle data extraction
        if response.data and len(response.data) > 0:
            image_url = response.data[0].url
            # Display the image
            st.image(image_url, caption=f'Your Custom {merch_type}')
        else:
            st.error("No image data found in response.")
    except Exception as e:
        st.error(f"Failed to generate design: {str(e)}")

