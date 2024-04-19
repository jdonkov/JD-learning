import streamlit as st
import os
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Step 2: Designing the UI Layout
st.title('Merch AI Designer: Revolutionizing Merchandise Creation')

# Step 3: Use Streamlit's sidebar for user input
st.sidebar.header("Design Customization")

# Step 4: User Inputs
description_input = st.sidebar.text_input("Describe your merch design:", "")
merch_type = st.sidebar.selectbox("Select Merchandise Type:",
                                  ['T-Shirt', 'Mug', 'Poster', 'Tote Bag',
                                   'Phone Case', 'Sticker', 'Pillow', 'Hoodie'])

# Step 5: Submit Button
submit_button = st.sidebar.button('Generate Design')

# Step 6: Processing User Inputs
if submit_button:
    # Generate Image using OpenAI API
    response = client.images.generate(
        prompt=description_input + " design on a " + merch_type,
        model="dall-e-3",
        size="1024x1024",
        quality="hd",
        n=1
    )

    # Accessing the image URL correctly:
    image_url = response.data[0].url

    # Display the image
    st.image(image_url, caption=f'Your Custom {merch_type}')

