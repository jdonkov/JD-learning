import streamlit as st
import os
import openai
import asyncio
from newsapi import NewsApiClient # Corrected from newsapi
from pydub import AudioSegment
import re
import json # Though not explicitly used in the main flow you provided, it's good practice for API interactions

# --- API Key Configuration ---
# For local testing, you might set environment variables directly.
# For Streamlit Cloud deployment, use st.secrets (see notes below script)

# Attempt to load API keys from Streamlit secrets
try:
    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
    NEWS_API_KEY = st.secrets["NEWS_API_KEY"]
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
except FileNotFoundError: # st.secrets file not found (e.g., local development)
    st.warning("Secrets file not found. Falling back to environment variables or manual input for API keys.")
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    NEWS_API_KEY = os.environ.get("NEWS_API_KEY")
    if not OPENAI_API_KEY or not NEWS_API_KEY:
        st.error("API keys not found in st.secrets or environment variables. Please set them up.")
        st.stop()
except KeyError: # One of the keys is missing in st.secrets
    st.error("One or more API keys are missing in st.secrets. Please ensure OPENAI_API_KEY and NEWS_API_KEY are set.")
    st.stop()


# Initialize the OpenAI client (globally or within the function that needs it)
# Ensure it's initialized after the API key is set
try:
    client = openai.AsyncOpenAI(api_key=OPENAI_API_KEY)
except Exception as e:
    st.error(f"Failed to initialize OpenAI client: {e}")
    st.stop()


# --- Agent Logic Functions (Copied from your Colab script) ---
async def scout_agent_run(topics: list[str]) -> list:
    """
    Agent 1: Finds news articles. This acts as our Retrieval Agent.
    """
    st.info(f"🕵️ Scout Agent: Searching for news on: {topics}...")
    try:
        # Use the NEWS_API_KEY variable directly
        newsapi_client = NewsApiClient(api_key=NEWS_API_KEY)
        query = " OR ".join(topics)
        # Using get_everything for potentially more diverse results, adjust as needed
        all_articles_data = await asyncio.to_thread(newsapi_client.get_everything, q=query, language='en', sort_by='relevancy', page_size=5)

        if all_articles_data['totalResults'] == 0:
            st.warning("Scout Agent: No articles found.")
            return []

        articles = [
            {"title": article['title'], "url": article['url'], "content": article.get('content', 'No content available.')}
            for article in all_articles_data['articles']
        ]
        st.info(f"Scout Agent: Found {len(articles)} articles.")
        return articles
    except Exception as e:
        st.error(f"❌ Scout Agent Error: {e}")
        return []

async def summarizer_agent_run(articles: list) -> list:
    """
    Agent 2: Summarizes articles. This acts as our Analysis/Creation Agent.
    """
    st.info(f"✍️ Summarizer Agent: Summarizing {len(articles)} articles...")
    summaries = []
    for article in articles:
        try:
            prompt = f"Please summarize the following article content for a daily news podcast. Keep it concise (2-3 sentences), focusing on the key takeaway. Article Title: {article['title']}\nContent: {article['content']}"
            response = await client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150,
            )
            summary = response.choices[0].message.content
            summaries.append({"title": article['title'], "summary": summary})
        except Exception as e:
            st.error(f"❌ Summarizer Agent Error for article '{article['title']}': {e}")
            summaries.append({"title": article['title'], "summary": "Could not summarize this article."})
    st.info(f"Summarizer Agent: Created {len(summaries)} summaries.")
    return summaries

async def producer_agent_run(summaries: list):
    """
    Agent 3: Creates a two-voice script and audio file.
    """
    st.info(f"🎙️ Producer Agent: Creating two-voice podcast script and audio file...")
    if not summaries:
        st.warning("Producer Agent: No summaries received. Halting process.")
        return None # Return None if no file is created

    try:
        summaries_text = "\n\n".join([f"Topic: {s['title']}\nSummary: {s['summary']}" for s in summaries])
        script_prompt = f"""
        You are an expert podcast scriptwriter for a tech show called 'Binary Break'.
        Your task is to create an engaging, conversational script between two hosts based on the provided summaries.

        THE HOSTS:
        - **Alex**: The main anchor. Knowledgeable, sets up the topics, and keeps the conversation flowing.
        - **Maya**: The color commentator. Witty, asks insightful questions, and offers relatable analogies.

        THE SUMMARIES:
        {summaries_text}

        RULES FOR THE SCRIPT:
        1.  **Create a Dialogue:** Create a real back-and-forth discussion. Maya should react to what Alex says and vice-versa.
        2.  **Invent Names:** You must use the host names Alex and Maya.
        3.  **Format Strictly:** Every line of dialogue must start with the host's name followed by a colon. Example: "Alex: Welcome to the show."
        4.  **SPOKEN WORDS ONLY:** Do NOT include any stage directions, sound effect cues, or any text in brackets.
        """
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": script_prompt}],
            max_tokens=800,
        )
        final_script = response.choices[0].message.content
        
        with st.expander("View Generated Script (v4 - Two-Host Dialogue)"):
            st.text_area("Script", final_script, height=300)

        st.info("🎙️ Starting two-voice audio generation...")
        host_voices = {
            "Alex": "onyx",
            "Maya": "shimmer"
        }
        script_lines = []
        for line in final_script.strip().split('\n'):
            if line.strip():
                match = re.match(r'^(Alex|Maya):\s*(.*)', line)
                if match:
                    host, dialogue = match.groups()
                    script_lines.append({"host": host, "dialogue": dialogue})

        segment_files = []
        combined_audio = AudioSegment.empty()

        for i, line_data in enumerate(script_lines):
            host = line_data["host"]
            dialogue = line_data["dialogue"]
            voice = host_voices.get(host)
            if not voice or not dialogue.strip(): # Skip empty dialogue lines
                continue

            st.info(f"Generating segment {i+1}/{len(script_lines)} for {host}...")
            try:
                tts_response = await client.audio.speech.create(
                    model="tts-1",
                    voice=voice,
                    input=dialogue
                )
                # Instead of saving to temp file, process in memory if possible or manage temp files carefully
                segment_audio = AudioSegment.from_file(tts_response.iter_bytes(), format="mp3")
                combined_audio += segment_audio
            except Exception as e:
                st.error(f"Error generating audio segment for {host}: {e}")
                continue # Skip this segment

        if len(combined_audio) > 0:
            final_filename = "podcast_final_two_voice.mp3"
            combined_audio.export(final_filename, format="mp3")
            st.success(f"✅ Success! Two-voice podcast created: {final_filename}")
            return final_filename
        else:
            st.warning("No audio segments were generated. Podcast creation failed.")
            return None

    except Exception as e:
        st.error(f"❌ Producer Agent Error: {e}")
        return None

# --- Streamlit UI ---
st.title("🎙️ AI Two-Voice Podcast Creator")

# Using session state to keep track of the generated file and generation status
if 'podcast_file' not in st.session_state:
    st.session_state.podcast_file = None
if 'is_generating' not in st.session_state:
    st.session_state.is_generating = False

topics_input = st.text_input("Enter topics for your podcast (separated by commas):", placeholder="e.g., AI safety, developments in fusion energy")

async def run_podcast_creation_workflow(topics_str):
    st.session_state.is_generating = True
    st.session_state.podcast_file = None # Reset previous file

    if not topics_str.strip():
        st.warning("Please enter some topics.")
        st.session_state.is_generating = False
        return

    topics_list = [topic.strip() for topic in topics_str.split(',')]
    
    with st.spinner("Generating your podcast... This might take a few minutes..."):
        articles_found = await scout_agent_run(topics_list)
        if articles_found:
            summaries_created = await summarizer_agent_run(articles_found)
            if summaries_created:
                podcast_filename_output = await producer_agent_run(summaries_created)
                st.session_state.podcast_file = podcast_filename_output
        else:
            st.warning("Could not find articles for the given topics.")
    
    st.session_state.is_generating = False


if st.button("Generate Podcast", disabled=st.session_state.is_generating):
    # We need to run the async function. Streamlit handles the loop.
    asyncio.run(run_podcast_creation_workflow(topics_input))


if st.session_state.podcast_file:
    st.subheader("Listen to Your Podcast:")
    try:
        audio_file = open(st.session_state.podcast_file, 'rb')
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format='audio/mp3')

        with open(st.session_state.podcast_file, "rb") as fp:
            st.download_button(
                label="Download Podcast MP3",
                data=fp,
                file_name=st.session_state.podcast_file,
                mime="audio/mpeg"
            )
    except FileNotFoundError:
        st.error("Generated podcast file not found. Please try generating again.")
    except Exception as e:
        st.error(f"Error displaying audio: {e}")

st.markdown("---")
st.markdown("Built by an AI Agent enthusiast!")
