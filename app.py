import streamlit as st
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import WebshareProxyConfig

prompt="""You are Yotube video summarizer. You will be taking the transcript text
and summarizing the entire video and providing the important summary in points
within 250 words. Please provide the summary of the text given here:  """

## getting the transcript data from yt videos
def extract_transcript_details(youtube_video_url):
    try:
        video_id=youtube_video_url.split("=")[1]

        ytt_api = YouTubeTranscriptApi(
            proxy_config=WebshareProxyConfig(
            proxy_username="slpbnhpc-rotate",
            proxy_password="9potzypj8ipy",
            )
        )

        # all requests done by ytt_api will now be proxied through Webshare
        transcript_text=ytt_api.get_transcript(video_id)
        
        # transcript_text=YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript

    except Exception as e:
        raise e
    
## getting the summary based on Prompt from Google Gemini Pro
def generate_gemini_content(transcript_text,prompt):

    model=genai.GenerativeModel("gemma-3n-e4b-it")
    response=model.generate_content(prompt+transcript_text)
    return response.text

## streamlit APP
st.set_page_config(page_title="Summarize From YouTube", page_icon="🤖")
st.title("YouTube Transcript to Detailed Notes Converter")
youtube_link = st.text_input("Enter YouTube Video Link:")

## Get the Google API Key and Url(YouTube)to be summarized
with st.sidebar:
    google_api_key=st.text_input("Google API Key",value="AIzaSyBad1oXrcnGNPdY6LkKWlaeZgCwjWIRfqQ",type="password")
    genai.configure(api_key=google_api_key)

if youtube_link:
    video_id = youtube_link.split("=")[1]
    print(video_id)
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_container_width=True)

if st.button("Get Detailed Notes"):
    if not youtube_link:
        st.write("Please enter a valid YouTube video link.")
    else:
        with st.spinner("Fetching transcript and generating summary..."):
            transcript_text=extract_transcript_details(youtube_link)

            if transcript_text:
                summary=generate_gemini_content(transcript_text,prompt)
                st.markdown("## Detailed Notes:")
                st.write(summary)





