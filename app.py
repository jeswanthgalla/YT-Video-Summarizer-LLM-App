import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
#loading environment variables 
#store the google api key obtained from https://aistudio.google.com/app/apikey with name "GOOGLE_API_KEY" in a .env file
load_dotenv()
 
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#Modify the prompt as per the requirement
new_prompt = """Assume you are a YouTube video summarizer and your task is to analyze the transcript text provided 
          and condense the entire video into concise points, ensuring that the summary remains within 250 words  """

def get_transcript(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript
    except Exception as e:
        raise e

def generate_summary(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt + transcript_text)
    return response.text

st.title("YouTube Transcript to Notes Converter")
youtube_link = st.text_input("Enter YouTube Video Link:")

if youtube_link:
    video_id = youtube_link.split("=")[1]
    print(video_id)
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Get Detailed Notes"):
    transcript_text = get_transcript(youtube_link)
    if transcript_text:
        summary = generate_summary(transcript_text, new_prompt)
        st.markdown("## Detailed Notes:")
        st.write(summary)
