import io
import cv2
import time
import base64
import requests
import tempfile
from PIL import Image
import streamlit as st
from pytube import YouTube

from api import *

def main():

    # Custom CSS to style placeholder text
    st.markdown(
        """
        <style>
        input::placeholder {
            color: grey;
            opacity: 0.6; 
        }
        .stButton { 
            display: flex;
            justify-content: center;
        }
        .centered-image {
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 50%; 
        }
        .centered-video {
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 80%;
        }
        </style>
        """,
        unsafe_allow_html=True
    ) 

    st.title("Avensz.Ai Homework Assignment")
    st.write("Hello World!")
    
    with st.form("video-upload"):
        st.write("Upload a file or enter a URL:")
        uploaded_video_file = st.file_uploader("Choose a video to upload! 🎞️", type=["mp4"])
        uploaded_audio_file = st.file_uploader("Choose an audio file to sync with your video!", type=["mp3", "wav"])
        # url_video_input = st.text_input("Copy & Paste the URL of the video you wish to upload 👇", placeholder="")
        # url_audio_input = st.text_input("Copy & Paste the URL of the audio you wish to sync 👇", placeholder="")
        submit_button = st.form_submit_button(label='Submit')

        if submit_button:
            if uploaded_video_file and uploaded_audio_file:
                st.success(f"File '{uploaded_video_file.name}' uploaded successfully!")
                video_processor_file(uploaded_video_file, uploaded_audio_file)
            # elif url_video_input and url_audio_input:
            #     st.success(f"URL '{url_video_input}' submitted successfully!")
            #     video_processor_link(url_video_input,url_audio_input)
            else:
                st.error("Please provide both a video file and an audio file")

    return None

def video_processor_file(video_file, audio_file):
    
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(video_file.read())

    vidcap = cv2.VideoCapture(tfile.name)
    success, image = vidcap.read()
    
    if success:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(image)
        
        buffered = io.BytesIO()
        pil_image.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode()

        image_html = f"""
        <div>
            <img src="data:image/png;base64,{img_base64}" class="centered-image" alt="Video Thumbnail"/>
        </div>
        """
        st.markdown(image_html, unsafe_allow_html=True)
        
    video_url, audio_url = upload_to_supabase(video_file,audio_file)
    
    st.info("Processing video...")
    progress_bar = st.progress(0)

    for percent_complete in range(100):
        time.sleep(0.1)  # Simulate some processing time
        progress_bar.progress(percent_complete + 1)

    result_url = post_lipsync(video_url,audio_url)

    # Step 4: Embed the video using HTML and base64
    video_html = f"""
    <div style="display: flex; justify-content: center;">
        <video width="500" controls>
            <source src="{result_url}" type="video/mp4">
            Your browser does not support the video tag.
        </video>
    </div>
    """
    st.markdown(video_html, unsafe_allow_html=True)

    return None

def video_processor_link(video_link, audio_link):
    
    try:
        yt = YouTube(video_link)
        thumbnail_url = yt.thumbnail_url
        
        # Fetch the thumbnail image
        response = requests.get(thumbnail_url)
        image = Image.open(io.BytesIO(response.content))

        # Display thumbnail
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode()
        
        image_html = f"""
        <div>
            <img src="data:image/png;base64,{img_base64}" class="centered-image" alt="Video Thumbnail"/>
        </div>
        """
        st.markdown(image_html, unsafe_allow_html=True)

        if yt:
            st.info("Processing video...")
            progress_bar = st.progress(0)

            for percent_complete in range(100):
                time.sleep(0.05)  # Simulate some processing time
                progress_bar.progress(percent_complete + 1)
            
            # Display the YouTube video using an iframe
            video_html = f"""
            <div>
                <iframe class="centered-video" width="560" height="315" src="https://www.youtube.com/embed/{yt.video_id}" frameborder="0" allowfullscreen></iframe>
            </div>
            """
            st.markdown(video_html, unsafe_allow_html=True)
            
            return None
        
    except Exception as e:
        st.error(f"Error fetching thumbnail: {e}")
        return None
    
    

if __name__ == '__main__':
    
    main()
    